# Criando scripts de configuração e arquivos adicionais

import os

# Criar diretório static
os.makedirs('static', exist_ok=True)

# Script SQL para criação do banco de dados MySQL
mysql_script = '''-- Script de criação do banco de dados MySQL
-- Sistema de Pesquisa de Satisfação - Hospital Santa Clara

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS hospital_satisfaction 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE hospital_satisfaction;

-- Tabela de pesquisas principais
CREATE TABLE surveys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255) NULL COMMENT 'Nome do paciente (NULL se anônimo)',
    is_anonymous BOOLEAN DEFAULT FALSE COMMENT 'Se a pesquisa é anônima',
    admission_date VARCHAR(50) NOT NULL COMMENT 'Data de internação',
    discharge_date VARCHAR(50) NOT NULL COMMENT 'Data de alta',
    observations TEXT NULL COMMENT 'Observações e comentários',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de criação da pesquisa',
    completed BOOLEAN DEFAULT FALSE COMMENT 'Se a pesquisa foi concluída',
    satisfaction_score DECIMAL(3,2) NULL COMMENT 'Pontuação média de satisfação',
    
    INDEX idx_created_at (created_at),
    INDEX idx_completed (completed),
    INDEX idx_satisfaction_score (satisfaction_score)
) COMMENT = 'Pesquisas de satisfação dos pacientes';

-- Tabela de perguntas do questionário
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id VARCHAR(10) UNIQUE NOT NULL COMMENT 'ID da pergunta (q1_1, q1_2, etc)',
    section_title VARCHAR(255) NOT NULL COMMENT 'Título da seção',
    question_text TEXT NOT NULL COMMENT 'Texto da pergunta',
    question_type VARCHAR(50) NOT NULL COMMENT 'Tipo da pergunta (satisfaction_scale, yes_no_partial, yes_no)',
    section_order INT NOT NULL COMMENT 'Ordem da seção',
    question_order INT NOT NULL COMMENT 'Ordem da pergunta na seção',
    
    INDEX idx_question_id (question_id),
    INDEX idx_section_order (section_order, question_order)
) COMMENT = 'Perguntas do questionário de satisfação';

-- Tabela de opções de resposta para cada pergunta
CREATE TABLE question_options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    option_text VARCHAR(255) NOT NULL COMMENT 'Texto da opção',
    option_value INT NOT NULL COMMENT 'Valor numérico para cálculos',
    option_order INT NOT NULL COMMENT 'Ordem da opção',
    
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    INDEX idx_question_id (question_id),
    INDEX idx_option_order (option_order)
) COMMENT = 'Opções de resposta para cada pergunta';

-- Tabela de respostas individuais
CREATE TABLE survey_responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    survey_id INT NOT NULL,
    question_id INT NOT NULL,
    response_value VARCHAR(255) NOT NULL COMMENT 'Resposta textual',
    response_score INT NULL COMMENT 'Pontuação numérica da resposta',
    
    FOREIGN KEY (survey_id) REFERENCES surveys(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    INDEX idx_survey_id (survey_id),
    INDEX idx_question_id (question_id),
    INDEX idx_response_score (response_score),
    
    UNIQUE KEY unique_survey_question (survey_id, question_id)
) COMMENT = 'Respostas individuais para cada pergunta da pesquisa';

-- Inserir perguntas padrão do questionário
INSERT INTO questions (question_id, section_title, question_text, question_type, section_order, question_order) VALUES
-- Seção 1: Atendimento
('q1_1', 'Seção 1: Atendimento', '1. Como você avaliaria a qualidade do atendimento recebido no hospital?', 'satisfaction_scale', 1, 1),
('q1_2', 'Seção 1: Atendimento', '2. Os profissionais de saúde foram atenciosos e respeitosos com você?', 'yes_no_partial', 1, 2),
('q1_3', 'Seção 1: Atendimento', '3. Você sentiu que suas necessidades foram atendidas de forma eficaz?', 'yes_no_partial', 1, 3),

-- Seção 2: Instalações e recursos
('q2_1', 'Seção 2: Instalações e recursos', '1. Como você avaliaria as instalações do hospital (limpeza, conforto, etc.)?', 'satisfaction_scale', 2, 1),
('q2_2', 'Seção 2: Instalações e recursos', '2. Os equipamentos e recursos disponíveis no hospital foram suficientes para o seu tratamento?', 'yes_no_partial', 2, 2),

-- Seção 3: Comunicação
('q3_1', 'Seção 3: Comunicação', '1. Você sentiu que os profissionais de saúde explicaram claramente o seu diagnóstico e tratamento?', 'yes_no_partial', 3, 1),
('q3_2', 'Seção 3: Comunicação', '2. Você foi informado sobre os seus direitos e responsabilidades como paciente?', 'yes_no_partial', 3, 2),

-- Seção 4: Filantropia e apoio
('q4_1', 'Seção 4: Filantropia e apoio', '1. Você sabe que o hospital é filantrópico e que sua missão é ajudar aqueles que não têm recursos?', 'yes_no', 4, 1),
('q4_2', 'Seção 4: Filantropia e apoio', '2. Você sente que o hospital está fazendo uma diferença positiva na comunidade?', 'yes_no_partial', 4, 2),

-- Seção 5: Recomendação
('q5_1', 'Seção 5: Recomendação', '1. Você recomendaria este hospital para amigos e familiares?', 'yes_no_partial', 5, 1);

-- Inserir opções de resposta para as perguntas
-- Perguntas de escala de satisfação (q1_1, q2_1)
INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Muito satisfeito(a)', 5, 1 FROM questions q WHERE q.question_id IN ('q1_1', 'q2_1');

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Satisfeito(a)', 4, 2 FROM questions q WHERE q.question_id IN ('q1_1', 'q2_1');

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Neutro(a)', 3, 3 FROM questions q WHERE q.question_id IN ('q1_1', 'q2_1');

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Insatisfeito(a)', 2, 4 FROM questions q WHERE q.question_id IN ('q1_1', 'q2_1');

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Muito insatisfeito(a)', 1, 5 FROM questions q WHERE q.question_id IN ('q1_1', 'q2_1');

-- Perguntas Sim/Não/Em parte (q1_2, q1_3, q2_2, q3_1, q3_2, q4_2, q5_1)
INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Sim', 5, 1 FROM questions q WHERE q.question_id IN ('q1_2', 'q1_3', 'q2_2', 'q3_1', 'q3_2', 'q4_2', 'q5_1');

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Não', 1, 2 FROM questions q WHERE q.question_id IN ('q1_2', 'q1_3', 'q2_2', 'q3_1', 'q3_2', 'q4_2', 'q5_1');

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Em parte', 3, 3 FROM questions q WHERE q.question_id IN ('q1_2', 'q1_3', 'q2_2', 'q3_1', 'q3_2', 'q4_2', 'q5_1');

-- Pergunta apenas Sim/Não (q4_1)
INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Sim', 5, 1 FROM questions q WHERE q.question_id = 'q4_1';

INSERT INTO question_options (question_id, option_text, option_value, option_order) 
SELECT q.id, 'Não', 1, 2 FROM questions q WHERE q.question_id = 'q4_1';

-- Criar views para facilitar consultas analíticas

-- View de satisfação por seção
CREATE VIEW satisfaction_by_section AS
SELECT 
    q.section_title,
    AVG(sr.response_score) as avg_satisfaction,
    COUNT(sr.id) as total_responses,
    COUNT(DISTINCT sr.survey_id) as unique_surveys
FROM questions q
JOIN survey_responses sr ON q.id = sr.question_id
WHERE sr.response_score IS NOT NULL
GROUP BY q.section_title
ORDER BY avg_satisfaction DESC;

-- View de tendência mensal
CREATE VIEW monthly_satisfaction AS
SELECT 
    DATE_FORMAT(s.created_at, '%Y-%m') as month,
    AVG(s.satisfaction_score) as avg_satisfaction,
    COUNT(s.id) as survey_count
FROM surveys s
WHERE s.completed = TRUE AND s.satisfaction_score IS NOT NULL
GROUP BY DATE_FORMAT(s.created_at, '%Y-%m')
ORDER BY month;

-- View de detalhes completos das pesquisas
CREATE VIEW survey_details AS
SELECT 
    s.id,
    s.patient_name,
    s.is_anonymous,
    s.admission_date,
    s.discharge_date,
    s.observations,
    s.created_at,
    s.satisfaction_score,
    COUNT(sr.id) as total_responses
FROM surveys s
LEFT JOIN survey_responses sr ON s.id = sr.survey_id
WHERE s.completed = TRUE
GROUP BY s.id, s.patient_name, s.is_anonymous, s.admission_date, 
         s.discharge_date, s.observations, s.created_at, s.satisfaction_score
ORDER BY s.created_at DESC;

-- Inserir dados de exemplo para demonstração
INSERT INTO surveys (patient_name, is_anonymous, admission_date, discharge_date, observations, completed, satisfaction_score, created_at) VALUES
('Maria Silva', FALSE, '2025-09-20', '2025-09-22', 'Excelente atendimento da equipe de enfermagem!', TRUE, 4.8, '2025-09-23 10:30:00'),
(NULL, TRUE, '2025-09-19', '2025-09-21', '', TRUE, 3.2, '2025-09-23 14:15:00'),
('João Pereira', FALSE, '2025-09-18', '2025-09-20', 'Poderiam melhorar a comunicação sobre os procedimentos.', TRUE, 3.8, '2025-09-22 16:45:00'),
(NULL, TRUE, '2025-09-17', '2025-09-19', 'Hospital muito limpo e organizado.', TRUE, 4.5, '2025-09-22 09:20:00'),
('Ana Costa', FALSE, '2025-09-16', '2025-09-18', '', TRUE, 4.2, '2025-09-21 11:10:00');

COMMIT;

-- Criar usuário específico para a aplicação (opcional)
-- CREATE USER 'hospital_app'@'localhost' IDENTIFIED BY 'secure_password_2025';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON hospital_satisfaction.* TO 'hospital_app'@'localhost';
-- FLUSH PRIVILEGES;

SELECT 'Banco de dados criado com sucesso!' as status;
'''

# Arquivo requirements.txt
requirements = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pymysql==1.1.0
python-multipart==0.0.6
jinja2==3.1.2
python-dotenv==1.0.0
alembic==1.12.1
cryptography==41.0.7
'''

# Arquivo .env de exemplo
env_example = '''# Configurações do Banco de Dados
DATABASE_URL=mysql+pymysql://hospital_app:secure_password_2025@localhost/hospital_satisfaction

# Para desenvolvimento local com SQLite (descomente a linha abaixo)
# DATABASE_URL=sqlite:///./hospital_satisfaction.db

# Configurações da Aplicação
APP_NAME="Sistema de Pesquisa de Satisfação - Hospital Santa Clara"
APP_VERSION=1.0.0
DEBUG=True

# Configurações de Email (para envio de relatórios)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=noreply@hospitalsantaclaracolorado.com.br

# Configurações de Segurança
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Configurações do Hospital
HOSPITAL_NAME="Hospital Santa Clara"
HOSPITAL_EMAIL="ti@hospitalsantaclaracolorado.com.br"
'''

# Dockerfile
dockerfile = '''FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \\
    gcc \\
    default-libmysqlclient-dev \\
    pkg-config \\
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p static templates

# Expor porta
EXPOSE 8000

# Comando para executar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

# docker-compose.yml
docker_compose = '''version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=mysql+pymysql://hospital_user:hospital_pass@db/hospital_satisfaction
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: hospital_satisfaction
      MYSQL_USER: hospital_user
      MYSQL_PASSWORD: hospital_pass
      MYSQL_ROOT_PASSWORD: root_password_change_me
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database_setup.sql:/docker-entrypoint-initdb.d/setup.sql
    restart: unless-stopped

  phpmyadmin:
    image: phpmyadmin:latest
    ports:
      - "8080:80"
    environment:
      PMA_HOST: db
      PMA_USER: hospital_user
      PMA_PASSWORD: hospital_pass
    depends_on:
      - db
    restart: unless-stopped

volumes:
  mysql_data:
'''

# Script de inicialização
start_script = '''#!/bin/bash

# Script de inicialização do Sistema de Pesquisa de Satisfação
# Hospital Santa Clara

echo "🏥 Iniciando Sistema de Pesquisa de Satisfação - Hospital Santa Clara"
echo "=================================================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "⬇️ Instalando dependências..."
pip install -r requirements.txt

# Verificar se arquivo .env existe
if [ ! -f ".env" ]; then
    echo "⚙️ Criando arquivo .env a partir do exemplo..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Configure o arquivo .env com suas credenciais!"
fi

# Executar aplicação
echo "🚀 Iniciando aplicação..."
echo ""
echo "📱 Interface da Pesquisa: http://localhost:8000"
echo "📊 Dashboard de Insights: http://localhost:8000/dashboard"
echo "🔧 Documentação da API: http://localhost:8000/docs"
echo ""
echo "Para parar a aplicação, pressione Ctrl+C"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
'''

# README.md
readme = '''# Sistema de Pesquisa de Satisfação - Hospital Santa Clara

![Hospital Santa Clara](https://img.shields.io/badge/Hospital-Santa%20Clara-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Python](https://img.shields.io/badge/Python-3.11-blue)

Sistema completo para coleta e análise de pesquisas de satisfação de pacientes, desenvolvido especificamente para o Hospital Santa Clara de Colorado.

## ✨ Funcionalidades

### 📱 Interface de Pesquisa (Tablet)
- Formulário otimizado para tablets
- Progresso em tempo real com mensagens motivacionais
- 5 seções de avaliação: Atendimento, Instalações, Comunicação, Filantropia e Recomendação
- Opção de pesquisa anônima
- Design responsivo e acessível

### 📊 Dashboard de Insights (Diretoria)
- Métricas principais em tempo real
- Gráficos de tendência e distribuição
- Análise por seção do questionário
- Insights automáticos e recomendações
- Relatórios exportáveis

### 🗄️ Backend Robusto
- API RESTful com FastAPI
- Banco de dados MySQL otimizado
- Validação de dados com Pydantic
- Sistema de logs e monitoramento

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.8 ou superior
- MySQL 8.0 ou superior
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/hospital-satisfaction-survey.git
cd hospital-satisfaction-survey
```

### 2. Configuração com Docker (Recomendado)
```bash
# Executar com Docker Compose
docker-compose up -d

# Acessar aplicação
open http://localhost:8000
```

### 3. Configuração Manual

#### 3.1 Configurar ambiente Python
```bash
# Executar script de inicialização
chmod +x start.sh
./start.sh
```

#### 3.2 Configurar banco de dados
```bash
# Executar script SQL no MySQL
mysql -u root -p < database_setup.sql

# Ou importar via phpMyAdmin
# http://localhost:8080
```

#### 3.3 Configurar variáveis de ambiente
```bash
# Copiar arquivo de configuração
cp .env.example .env

# Editar com suas configurações
nano .env
```

#### 3.4 Executar aplicação
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🎯 Como Usar

### Para Equipe de Campo (Tablets)
1. Acesse `http://localhost:8000`
2. Preencha os dados do paciente
3. Percorra as 5 seções de perguntas
4. Adicione observações se necessário
5. Envie a pesquisa

### Para Diretoria (Dashboard)
1. Acesse `http://localhost:8000/dashboard`
2. Analise as métricas principais
3. Verifique os gráficos de tendência
4. Revise insights e recomendações
5. Exporte relatórios conforme necessário

## 📁 Estrutura do Projeto

```
hospital-satisfaction-survey/
├── main.py                 # Aplicação principal FastAPI
├── templates/             # Templates HTML
│   ├── base.html         # Template base
│   ├── survey.html       # Interface da pesquisa
│   └── dashboard.html    # Dashboard de insights
├── static/               # Arquivos estáticos (CSS, JS, imagens)
├── database_setup.sql    # Script de configuração do MySQL
├── requirements.txt      # Dependências Python
├── .env.example         # Exemplo de configurações
├── Dockerfile           # Configuração Docker
├── docker-compose.yml   # Orquestração de containers
├── start.sh            # Script de inicialização
└── README.md           # Este arquivo
```

## 🔧 Configuração

### Banco de Dados MySQL
O sistema cria automaticamente as seguintes tabelas:
- `surveys` - Pesquisas principais
- `questions` - Perguntas do questionário  
- `question_options` - Opções de resposta
- `survey_responses` - Respostas individuais

### Variáveis de Ambiente (.env)
```env
DATABASE_URL=mysql+pymysql://user:password@localhost/hospital_satisfaction
APP_NAME="Sistema de Pesquisa - Hospital Santa Clara"
DEBUG=True
HOSPITAL_EMAIL=ti@hospitalsantaclaracolorado.com.br
```

## 📊 API Endpoints

### Principais Rotas
- `GET /` - Interface de pesquisa
- `GET /dashboard` - Dashboard de insights
- `POST /api/submit-survey` - Submeter pesquisa
- `GET /api/dashboard-data` - Dados do dashboard
- `GET /api/questions` - Listar perguntas
- `GET /docs` - Documentação da API

## 🎨 Personalização

### Cores e Tema
Edite as variáveis CSS no arquivo `templates/base.html`:
```css
:root {
    --primary-color: #2980b9;
    --secondary-color: #3498db;
    --success-color: #27ae60;
    /* ... */
}
```

### Perguntas do Questionário
Modifique o script `database_setup.sql` para personalizar perguntas e opções.

### Logo do Hospital
Substitua o placeholder SVG em `templates/survey.html` pela logo real.

## 📈 Analytics e Insights

O sistema gera automaticamente:
- **Métricas principais**: Total de respostas, satisfação média, taxa de resposta
- **Análise temporal**: Tendências mensais e evolução
- **Análise setorial**: Performance por área do hospital
- **Insights automáticos**: Pontos fortes e oportunidades de melhoria
- **Recomendações**: Ações sugeridas baseadas nos dados

## 🛠️ Desenvolvimento

### Estrutura do Código
- **Modelos de Dados**: SQLAlchemy com MySQL
- **API**: FastAPI com validação Pydantic
- **Frontend**: HTML/CSS/JavaScript com Bootstrap
- **Charts**: Chart.js para visualizações
- **Templates**: Jinja2 para renderização

### Executar em Modo de Desenvolvimento
```bash
# Com reload automático
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Com debug
uvicorn main:app --reload --log-level debug
```

## 📦 Deploy em Produção

### Usando Docker
```bash
# Build da imagem
docker build -t hospital-survey .

# Executar container
docker run -d -p 8000:8000 hospital-survey
```

### Configurações de Produção
1. Altere `DEBUG=False` no `.env`
2. Configure SSL/HTTPS
3. Use um proxy reverso (nginx)
4. Configure backup automático do banco
5. Configure monitoramento e logs

## 🔐 Segurança

- Validação de dados no backend
- Proteção contra SQL Injection
- Sanitização de inputs
- Configuração segura do MySQL
- Logs de auditoria

## 📞 Suporte

Para dúvidas e suporte técnico:
- **Email**: ti@hospitalsantaclaracolorado.com.br
- **Documentação**: http://localhost:8000/docs
- **Issues**: Reporte problemas no GitHub

## 📄 Licença

Este projeto foi desenvolvido especificamente para o Hospital Santa Clara de Colorado.

---

**Desenvolvido com ❤️ para melhorar a experiência dos pacientes do Hospital Santa Clara**
'''

# Salvar todos os arquivos
with open('database_setup.sql', 'w', encoding='utf-8') as f:
    f.write(mysql_script)

with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(requirements)

with open('.env.example', 'w', encoding='utf-8') as f:
    f.write(env_example)

with open('Dockerfile', 'w', encoding='utf-8') as f:
    f.write(dockerfile)

with open('docker-compose.yml', 'w', encoding='utf-8') as f:
    f.write(docker_compose)

with open('start.sh', 'w', encoding='utf-8') as f:
    f.write(start_script)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme)

# Tornar o script executável (Linux/Mac)
try:
    os.chmod('start.sh', 0o755)
    print("✅ Script start.sh marcado como executável")
except:
    print("⚠️  Não foi possível marcar start.sh como executável (Windows?)")

print("✅ Arquivos de configuração criados com sucesso!")
print("\nArquivos criados:")
print("   - database_setup.sql    (Configuração MySQL)")
print("   - requirements.txt      (Dependências Python)")
print("   - .env.example         (Configurações de exemplo)")  
print("   - Dockerfile           (Container Docker)")
print("   - docker-compose.yml   (Orquestração)")
print("   - start.sh             (Script de inicialização)")
print("   - README.md            (Documentação completa)")
print("\n🎉 Projeto completo criado!")