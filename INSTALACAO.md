# 📦 Guia de Instalação - Sistema de Gestão de Concessionária

## Pré-requisitos

- Python 3.8 ou superior
- MySQL 8.0 ou superior
- Navegador web moderno

## Passo a Passo

### 1. Instalar Python (se necessário)

Download em: https://www.python.org/downloads/

### 2. Instalar MySQL (se necessário)

Download em: https://dev.mysql.com/downloads/installer/

### 3. Instalar Dependências Python

Abra o terminal na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

Ou se tiver Python 3 especificamente:

```bash
pip3 install -r requirements.txt
```

Se estiver no Windows e `pip` não funcionar, tente:

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados MySQL

1. Abra o MySQL Workbench ou MySQL Command Line
2. Execute o arquivo `SQL-Códigos-BD.txt` para criar o banco de dados
3. Ou execute os comandos abaixo:

```sql
CREATE DATABASE concessionaria CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE concessionaria;
```

Depois, abra o arquivo `SQL-Códigos-BD.txt` e copie todo o conteúdo, executando linha por linha no MySQL.

### 5. Configurar Conexão com o Banco

Edite o arquivo `config.py` com suas credenciais do MySQL:

```python
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Seu usuário MySQL
        password="sua_senha", # Sua senha MySQL
        database="concessionaria"
    )
```

### 6. Criar Pasta de Uploads

No terminal, na pasta do projeto:

**Windows (PowerShell):**
```powershell
mkdir static\uploads
```

**Linux/Mac:**
```bash
mkdir -p static/uploads
```

### 7. Executar a Aplicação

No terminal, na pasta do projeto:

```bash
python app.py
```

Ou se tiver Python 3:

```bash
python3 app.py
```

### 8. Acessar o Sistema

Abra seu navegador e acesse:

```
http://localhost:5000
```

## 📝 Credenciais Padrão

Após criar o banco de dados, você pode fazer login com:

- **Email:** admin@concessionaria.com
- **Senha:** admin123

**⚠️ IMPORTANTE:** Altere a senha padrão após o primeiro acesso!

## 🚨 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'flask'"

**Solução:** Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: "Can't connect to MySQL server"

**Solução:** 
1. Verifique se o MySQL está rodando
2. Confira as credenciais no arquivo `config.py`
3. Verifique se o banco de dados `concessionaria` foi criado

### Erro: "Table doesn't exist"

**Solução:** Execute novamente o arquivo `SQL-Códigos-BD.txt` no MySQL

### Erro: "Permission denied" ao fazer upload

**Solução (Linux/Mac):**
```bash
chmod 777 static/uploads
```

**Solução (Windows):**
Certifique-se de que a pasta `static/uploads` existe e tem permissão de escrita

## 📞 Suporte

Se encontrar problemas, verifique:
1. Se o Python está instalado: `python --version`
2. Se o MySQL está instalado: `mysql --version`
3. Se todas as dependências foram instaladas: `pip list`
4. Se o banco de dados foi criado corretamente

## ✅ Verificação de Instalação

Para verificar se tudo está funcionando:

1. A aplicação deve iniciar sem erros
2. Você deve conseguir acessar http://localhost:5000
3. Deve ver a página inicial
4. Deve conseguir fazer login com admin@concessionaria.com

---

**Boa sorte com seu projeto! 🚀**
