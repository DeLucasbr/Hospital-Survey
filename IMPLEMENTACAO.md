# Guia de Implementação Completo
## Sistema de Pesquisa de Satisfação - Hospital Santa Clara

Este guia fornece um passo a passo detalhado para implementar o sistema de pesquisa de satisfação no Hospital Santa Clara de Colorado.

## 🎯 Visão Geral do Sistema

O sistema foi desenvolvido seguindo as especificações do código React Native fornecido, mas migrado para uma aplicação web completa usando:

- **Backend**: FastAPI (Python) - Alta performance e fácil manutenção
- **Frontend**: HTML/CSS/JavaScript com Bootstrap - Interface responsiva e moderna
- **Banco de Dados**: MySQL - Robusto e confiável para ambiente hospitalar
- **Visualizações**: Chart.js - Gráficos interativos para insights
- **Deploy**: Docker - Facilita instalação e manutenção

## 🏗️ Arquitetura da Solução

### 1. Camada de Apresentação (Frontend)
- **Interface de Pesquisa**: Otimizada para tablets, replicando exatamente o layout do React Native
- **Dashboard de Insights**: Interface administrativa para análise dos dados
- **Design Responsivo**: Funciona em tablets, desktops e celulares

### 2. Camada de Aplicação (Backend)
- **API RESTful**: Endpoints para submissão de pesquisas e consulta de dados
- **Validação de Dados**: Garante integridade das informações
- **Cálculos Automáticos**: Pontuação de satisfação e estatísticas

### 3. Camada de Dados (Banco)
- **Estrutura Normalizada**: Otimizada para consultas analíticas
- **Views Pré-construídas**: Facilita geração de relatórios
- **Índices Otimizados**: Performance para grandes volumes

## 📋 Pré-requisitos de Instalação

### Opção 1: Instalação com Docker (Recomendada)
**Vantagens**: Instalação automática, isolamento, fácil backup

**Requisitos mínimos**:
- Docker e Docker Compose instalados
- 4GB RAM disponível
- 10GB espaço em disco
- Portas 8000, 3306, 8080 livres

### Opção 2: Instalação Manual
**Vantagens**: Mais controle, integração com sistemas existentes

**Requisitos**:
- Python 3.8+
- MySQL 8.0+
- 2GB RAM disponível
- 5GB espaço em disco

## 🚀 Instalação Passo a Passo

### OPÇÃO 1: Docker (Mais Simples)

#### Passo 1: Preparar ambiente
```bash
# 1. Baixar arquivos do projeto (substitua pelo método que você usará)
mkdir hospital-survey
cd hospital-survey

# 2. Colocar todos os arquivos do projeto na pasta
# (main.py, templates/, docker-compose.yml, etc.)
```

#### Passo 2: Executar
```bash
# 1. Iniciar containers
docker-compose up -d

# 2. Verificar se está funcionando
curl http://localhost:8000

# 3. Acessar aplicações
# Pesquisa: http://localhost:8000
# Dashboard: http://localhost:8000/dashboard
# Banco de dados: http://localhost:8080 (phpMyAdmin)
```

### OPÇÃO 2: Instalação Manual

#### Passo 1: Configurar MySQL
```bash
# 1. Instalar MySQL (Ubuntu/Debian)
sudo apt update
sudo apt install mysql-server

# 2. Configurar segurança
sudo mysql_secure_installation

# 3. Criar banco de dados
mysql -u root -p < database_setup.sql
```

#### Passo 2: Configurar Python
```bash
# 1. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 2. Instalar dependências
pip install -r requirements.txt
```

#### Passo 3: Configurar aplicação
```bash
# 1. Copiar configurações
cp .env.example .env

# 2. Editar configurações do banco
nano .env
# Alterar: DATABASE_URL=mysql+pymysql://user:password@localhost/hospital_satisfaction
```

#### Passo 4: Executar
```bash
# 1. Iniciar aplicação
uvicorn main:app --host 0.0.0.0 --port 8000

# 2. Testar
open http://localhost:8000
```

## ⚙️ Configurações Importantes

### 1. Configurações do Banco de Dados (.env)
```env
# Para MySQL local
DATABASE_URL=mysql+pymysql://hospital_user:senha_segura@localhost/hospital_satisfaction

# Para MySQL remoto
DATABASE_URL=mysql+pymysql://usuario:senha@servidor.hospital.com:3306/hospital_satisfaction

# Para desenvolvimento (SQLite)
DATABASE_URL=sqlite:///./hospital_satisfaction.db
```

### 2. Configurações de Email (para relatórios)
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=relatorios@hospitalsantaclaracolorado.com.br
SMTP_PASSWORD=sua_senha_de_app
SMTP_FROM=noreply@hospitalsantaclaracolorado.com.br
```

### 3. Configurações de Segurança (produção)
```env
DEBUG=False
SECRET_KEY=gere_uma_chave_secreta_forte_aqui
ALLOWED_HOSTS=seu-dominio.com,ip-do-servidor
```

## 📱 Como Usar o Sistema

### Para a Equipe de Enfermagem (Tablets)

1. **Acessar**: `http://ip-do-servidor:8000`
2. **Preencher dados do paciente**:
   - Nome (ou marcar "Anônimo")
   - Data de internação
   - Data de alta
3. **Responder questões**:
   - Seção 1: Atendimento (3 perguntas)
   - Seção 2: Instalações (2 perguntas)
   - Seção 3: Comunicação (2 perguntas)
   - Seção 4: Filantropia (2 perguntas)
   - Seção 5: Recomendação (1 pergunta)
4. **Adicionar observações** (opcional)
5. **Enviar pesquisa**

### Para a Diretoria (Dashboard)

1. **Acessar**: `http://ip-do-servidor:8000/dashboard`
2. **Visualizar métricas**:
   - Total de respostas
   - Satisfação média geral
   - Taxa de resposta
   - Crescimento mensal
3. **Analisar gráficos**:
   - Tendência de satisfação ao longo do tempo
   - Distribuição de níveis de satisfação
   - Comparação entre seções
4. **Revisar insights automáticos**:
   - Pontos fortes identificados
   - Áreas de melhoria
   - Recomendações de ação

## 📊 Interpretação dos Insights

### Métricas Principais
- **Satisfação Média**: Escala de 1-5, sendo 4+ considerado bom
- **Taxa de Resposta**: % de pacientes que respondem (meta: >80%)
- **Distribuição**: Idealmente >70% "Satisfeito" ou "Muito Satisfeito"

### Sinais de Alerta
- Satisfação média <3.5 em qualquer seção
- Tendência de queda por 2+ meses consecutivos
- Taxa de resposta <60%
- Aumento de comentários negativos

### Ações Recomendadas
- **Comunicação baixa**: Treinamento da equipe em comunicação clara
- **Instalações baixas**: Verificar limpeza e manutenção
- **Atendimento baixo**: Revisão de protocolos de atendimento
- **Filantropia baixa**: Melhorar comunicação da missão social

## 🔧 Manutenção e Monitoramento

### Backup Diário (Importante!)
```bash
# Backup automático MySQL
mysqldump -u root -p hospital_satisfaction > backup_$(date +%Y%m%d).sql

# Backup com Docker
docker exec mysql_container mysqldump -u root -p hospital_satisfaction > backup.sql
```

### Logs de Sistema
```bash
# Ver logs da aplicação
tail -f app.log

# Ver logs do Docker
docker-compose logs -f web
```

### Atualizações
```bash
# Parar sistema
docker-compose down

# Atualizar código
git pull  # se usando Git

# Reiniciar
docker-compose up -d
```

## 🚨 Solução de Problemas Comuns

### 1. "Connection refused" - Banco não conecta
```bash
# Verificar se MySQL está rodando
sudo systemctl status mysql

# Verificar configurações no .env
cat .env | grep DATABASE_URL

# Testar conexão manual
mysql -u usuario -p -h localhost
```

### 2. "Permission denied" - Problemas de acesso
```bash
# Verificar permissões de arquivos
ls -la templates/
chmod 755 templates/

# Verificar usuário MySQL
SHOW GRANTS FOR 'hospital_user'@'localhost';
```

### 3. "Internal Server Error" - Erro na aplicação
```bash
# Ver logs detalhados
uvicorn main:app --log-level debug

# Verificar dependências
pip list | grep fastapi
```

### 4. Interface não carrega no tablet
- Verificar se o tablet está na mesma rede
- Testar com IP específico: `http://192.168.1.100:8000`
- Verificar firewall do servidor
- Usar navegador atualizado (Chrome, Firefox)

## 📈 Otimizações de Performance

### Para muitos usuários simultâneos
```bash
# Usar Gunicorn com múltiplos workers
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Para banco de dados grande
```sql
-- Criar índices adicionais
CREATE INDEX idx_created_date ON surveys (DATE(created_at));
CREATE INDEX idx_section_score ON survey_responses (question_id, response_score);
```

### Proxy reverso (produção)
```nginx
# /etc/nginx/sites-available/hospital-survey
server {
    listen 80;
    server_name pesquisa.hospitalsantaclara.com.br;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔐 Segurança em Produção

### 1. SSL/HTTPS obrigatório
```bash
# Com Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d pesquisa.hospitalsantaclara.com.br
```

### 2. Firewall
```bash
# Permitir apenas portas necessárias
sudo ufw allow 22   # SSH
sudo ufw allow 80   # HTTP
sudo ufw allow 443  # HTTPS
sudo ufw enable
```

### 3. Backup automático
```bash
# Crontab para backup diário
0 2 * * * /home/usuario/backup_hospital.sh
```

## 📞 Contato e Suporte

Para implementação e suporte:
- **Email técnico**: ti@hospitalsantaclaracolorado.com.br
- **Documentação**: http://localhost:8000/docs (quando rodando)
- **Arquivos do projeto**: [incluir localização dos arquivos]

---

**Sistema desenvolvido especificamente para o Hospital Santa Clara de Colorado**
**Focado na praticidade e geração de insights valiosos para a diretoria**
