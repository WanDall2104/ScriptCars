# 🚗 Sistema de Gestão de Concessionária

Sistema completo de gestão para concessionária com CRUD de clientes, veículos, funcionários e vendas.

## 📋 Características

- ✅ CRUD completo para Clientes, Veículos, Funcionários e Vendas
- ✅ Sistema de autenticação com hash de senhas (bcrypt)
- ✅ Sessões persistentes com opção de "Lembrar Senha"
- ✅ Arquitetura MVC completa
- ✅ Sistema de upload de fotos de veículos
- ✅ Páginas públicas: Home, Sobre e Veículos Disponíveis
- ✅ Validações completas de dados
- ✅ Interface moderna e responsiva
- ✅ Banco de dados MySQL

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- MySQL 8.0+

### Passos

1. **Clone o repositório ou navegue até o diretório do projeto**

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure o banco de dados:**

   Edite o arquivo `config.py` com suas credenciais:
```python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="SEU_USUARIO",
        password="SUA_SENHA",
        database="concessionaria"
    )
```

4. **Crie o banco de dados:**

   Execute o arquivo `SQL-Códigos-BD.txt` no MySQL:
```bash
mysql -u root -p < SQL-Códigos-BD.txt
```

   Ou abra o arquivo `SQL-Códigos-BD.txt` e execute as queries no MySQL Workbench.

5. **Crie a pasta de uploads (se necessário):**
```bash
mkdir static/uploads
```

6. **Execute a aplicação:**
```bash
python app.py
```

7. **Acesse no navegador:**
```
http://localhost:5000
```

## 👤 Credenciais Padrão

Após executar o SQL, você pode fazer login com:
- **Email:** admin@concessionaria.com
- **Senha:** admin123

## 📁 Estrutura do Projeto

```
projetofinalbackend/
├── app.py                      # Arquivo principal da aplicação
├── config.py                   # Configuração do banco de dados
├── requirements.txt             # Dependências do projeto
├── SQL-Códigos-BD.txt          # Script de criação do banco de dados
├── controllers/                # Controllers (lógica de controle)
│   ├── auth_controller.py      # Autenticação e login
│   ├── cliente_controller.py   # CRUD de clientes
│   ├── funcionario_controller.py # CRUD de funcionários
│   ├── veiculo_controller.py   # CRUD de veículos
│   └── venda_controller.py      # CRUD de vendas
├── models/                     # Models (lógica de negócio)
│   ├── __init__.py
│   ├── cliente_model.py        # Funções de acesso aos dados de clientes
│   ├── funcionario_model.py    # Funções de acesso aos dados de funcionários
│   ├── veiculo_model.py        # Funções de acesso aos dados de veículos
│   └── venda_model.py          # Funções de acesso aos dados de vendas
├── views/                      # Templates (HTML)
│   ├── base.html               # Template base
│   ├── home.html               # Página inicial (pública)
│   ├── sobre.html              # Sobre a empresa (pública)
│   ├── login.html              # Página de login
│   ├── cadastro.html           # Página de cadastro
│   ├── veiculos_disponiveis.html # Veículos (pública)
│   ├── clientes.html           # Lista de clientes
│   ├── funcionarios.html       # Lista de funcionários
│   ├── veiculos.html           # Lista de veículos
│   ├── vendas.html             # Lista de vendas
│   └── form_*.html             # Formulários de CRUD
└── static/                     # Arquivos estáticos
    ├── css/
    │   └── style.css           # Estilos CSS
    └── uploads/                 # Fotos dos veículos
```

## 🎯 Funcionalidades

### Páginas Públicas (sem login)
- **Home:** Página inicial com informações sobre a concessionária
- **Sobre:** Informações detalhadas sobre a empresa
- **Veículos Disponíveis:** Catálogo de veículos disponíveis para venda

### Área Administrativa (requer login)
- **Clientes:** Gerenciar clientes (criar, editar, excluir, listar)
- **Veículos:** Gerenciar veículos com upload de fotos
- **Funcionários:** Gerenciar funcionários
- **Vendas:** Registrar e gerenciar vendas

### Sistema de Login
- Cadastro de funcionários com hash de senha
- Sessões com opção de "Lembrar Senha"
- Proteção de rotas administrativas
- Logout seguro

### Upload de Arquivos
- Upload de fotos de veículos
- Validação de tipo e tamanho de arquivo
- Armazenamento em `static/uploads/`

## 🔒 Segurança

- Senhas criptografadas com bcrypt
- Proteção contra SQL Injection usando parâmetros parametrizados
- Sessões seguras com chave secreta
- Validação de dados em todas as entradas
- Proteção de rotas administrativas

## ✅ Requisitos Mínimos Atendidos

- ✅ CRUD completo para 4 entidades (Clientes, Veículos, Funcionários, Vendas)
- ✅ Pelo menos 3 páginas abertas (Home, Sobre, Veículos)
- ✅ Sistema de Upload/Download de fotos de veículos
- ✅ Sistema de Login com hash de senhas
- ✅ Funcionalidade "Lembrar Senha"
- ✅ Uso de sessões
- ✅ Arquitetura MVC completa
- ✅ Validações completas de dados
- ✅ Estruturas de controle e laços
- ✅ HTML sem tags depreciadas
- ✅ CSS em todas as páginas
- ✅ JavaScript mínimo (<30% do código)
- ✅ Tabelas bem estruturadas no banco de dados
- ✅ Código modularizado

## 🛠️ Tecnologias Utilizadas

- **Backend:** Flask (Python)
- **Banco de Dados:** MySQL
- **Segurança:** bcrypt
- **Frontend:** HTML5, CSS3, JavaScript
- **Arquitetura:** MVC (Model-View-Controller)

## 📝 Observações

- O banco de dados usa MySQL. Certifique-se de que o MySQL está rodando antes de iniciar a aplicação.
- As fotos dos veículos são salvas na pasta `static/uploads/`. Certifique-se de que esta pasta existe e tem permissões de escrita.
- A senha padrão do admin é "admin123". Recomenda-se alterar para produção.

## 👨‍💻 Desenvolvido por

Projeto desenvolvido como projeto final da disciplina de Backend Development.

---

**Licença:** Este projeto é acadêmico e destinado a fins educacionais.
