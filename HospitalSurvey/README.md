# Sistema de Pesquisa de Satisfação - Hospital Santa Clara

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
