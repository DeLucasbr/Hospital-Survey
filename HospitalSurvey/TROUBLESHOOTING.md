# Guia de Solução de Problemas
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
curl -X POST http://localhost:8000/api/submit-survey \
  -H "Content-Type: application/x-www-form-urlencoded" \
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
