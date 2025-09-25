# Criar guia final de implementação

implementation_guide = '''# Guia de Implementação Completo
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
venv\\Scripts\\activate  # Windows

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
'''

# Criar arquivo de troubleshooting
troubleshooting = '''# Guia de Solução de Problemas
## Sistema de Pesquisa de Satisfação

## 🚨 Problemas Mais Comuns

### 1. Sistema não inicia
**Erro**: "Application startup failed"

**Soluções**:
```bash
# Verificar se todas as dependências estão instaladas
pip install -r requirements.txt

# Verificar configurações do .env
cat .env

# Testar conexão com banco
python -c "from sqlalchemy import create_engine; engine = create_engine('SEU_DATABASE_URL'); engine.connect()"
```

### 2. Banco de dados não conecta
**Erro**: "Can't connect to MySQL server"

**Soluções**:
```bash
# Verificar se MySQL está rodando
sudo systemctl status mysql
sudo systemctl start mysql

# Testar conexão manual
mysql -u root -p

# Verificar usuários e permissões
mysql -u root -p -e "SELECT user, host FROM mysql.user;"
```

### 3. Pesquisa não envia
**Erro**: Forms não funcionam

**Soluções**:
- Verificar se todas as perguntas foram respondidas
- Abrir console do navegador (F12) para ver erros JavaScript
- Verificar se o endpoint `/api/submit-survey` está funcionando
- Testar com curl:
```bash
curl -X POST http://localhost:8000/api/submit-survey -H "Content-Type: application/json" -d '{}'
```

### 4. Dashboard não carrega dados
**Erro**: Gráficos vazios

**Soluções**:
```bash
# Verificar se há dados no banco
mysql -u root -p hospital_satisfaction -e "SELECT COUNT(*) FROM surveys;"

# Testar endpoint de dados
curl http://localhost:8000/api/dashboard-data

# Verificar logs da aplicação
tail -f app.log
```

## 🔍 Diagnóstico Passo a Passo

### 1. Verificação Básica
```bash
# Sistema operacional
uname -a

# Python instalado
python3 --version

# MySQL instalado
mysql --version

# Espaço em disco
df -h

# Memória disponível
free -m

# Portas em uso
netstat -tlnp | grep :8000
```

### 2. Verificação da Aplicação
```bash
# Dependências Python
pip list | grep -E "(fastapi|sqlalchemy|pymysql)"

# Configurações
env | grep -E "(DATABASE|MYSQL)"

# Logs de erro
tail -n 50 app.log

# Teste de conectividade
curl -I http://localhost:8000
```

### 3. Verificação do Banco
```sql
-- Conectar no MySQL
mysql -u root -p

-- Verificar banco
SHOW DATABASES;
USE hospital_satisfaction;

-- Verificar tabelas
SHOW TABLES;

-- Verificar dados
SELECT COUNT(*) FROM surveys;
SELECT COUNT(*) FROM questions;
SELECT COUNT(*) FROM survey_responses;

-- Verificar usuários
SELECT user, host FROM mysql.user WHERE user LIKE 'hospital%';
```

## 🔧 Ferramentas de Debug

### 1. Modo Debug da Aplicação
```python
# Em main.py, adicionar no final:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
```

### 2. Logs Detalhados
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Adicionar no início de main.py
```

### 3. Teste Manual das APIs
```bash
# Testar endpoint de questões
curl http://localhost:8000/api/questions

# Testar submissão de pesquisa
curl -X POST http://localhost:8000/api/submit-survey \\
  -H "Content-Type: application/x-www-form-urlencoded" \\
  -d "patient_name=Teste&admission_date=2025-01-01&discharge_date=2025-01-02&q1_1=Satisfeito(a)"

# Testar dados do dashboard
curl http://localhost:8000/api/dashboard-data
```

## 📱 Problemas Específicos do Tablet

### Tela não se adapta
- Verificar meta viewport no HTML
- Testar diferentes navegadores
- Verificar CSS responsivo

### Touch não funciona adequadamente
- Aumentar tamanho dos botões/checkboxes
- Verificar z-index de elementos
- Testar com diferentes tablets

### Lentidão na interface
- Otimizar JavaScript
- Reduzir tamanho das imagens
- Verificar conexão de rede

## 🌐 Problemas de Rede

### Aplicação não acessível
```bash
# Verificar se está ouvindo na porta correta
netstat -tlnp | grep 8000

# Verificar firewall
sudo ufw status

# Testar localmente primeiro
curl http://127.0.0.1:8000

# Depois testar por IP
curl http://IP-DO-SERVIDOR:8000
```

### Timeout de conexão
- Aumentar timeouts do MySQL
- Verificar latência de rede
- Otimizar consultas SQL

## 💾 Recuperação de Dados

### Backup corrompido
```bash
# Verificar integridade
mysql < backup.sql --force

# Recuperar tabelas específicas
mysql hospital_satisfaction < backup_questions.sql
```

### Dados perdidos
```sql
-- Verificar logs do MySQL
SHOW VARIABLES LIKE 'general_log%';

-- Recuperar de backups parciais
-- (sempre manter múltiplos backups!)
```

## 📞 Quando Pedir Ajuda

Entre em contato se:
- Problemas persistem após tentar as soluções
- Erro crítico que afeta operação
- Necessidade de personalização
- Dúvidas sobre interpretação de dados

**Inclua sempre**:
- Sistema operacional
- Versão do Python e MySQL
- Mensagem de erro completa
- Logs relevantes
- Passos para reproduzir o problema

---

**Lembre-se**: A maioria dos problemas tem solução simples. Siga o passo a passo e não hesite em pedir ajuda!
'''

# Salvar os guias
with open('IMPLEMENTACAO.md', 'w', encoding='utf-8') as f:
    f.write(implementation_guide)

with open('TROUBLESHOOTING.md', 'w', encoding='utf-8') as f:
    f.write(troubleshooting)

print("✅ Guias adicionais criados:")
print("   - IMPLEMENTACAO.md  (Guia completo de implementação)")
print("   - TROUBLESHOOTING.md (Solução de problemas)")
print("\n🎯 Sistema completo desenvolvido!")
print("\nPróximos passos recomendados:")
print("1. Revisar a aplicação web criada: hospital-satisfaction-survey")
print("2. Configurar servidor MySQL")
print("3. Personalizar templates conforme necessário")
print("4. Testar em tablets do hospital")
print("5. Treinar equipe para uso")
print("6. Implementar em produção")
print("\n💡 O sistema replica exatamente as funcionalidades do React Native")
print("   mas com vantagens de uma aplicação web gerenciada pelo FastAPI!")