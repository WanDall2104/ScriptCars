import bcrypt
from config import Config
from config import inicia_bd


# FUNÇÃO CORRETA PARA PROFESSOR
def listar_clientes():
    """Lista todos os clientes"""
    conn = Config.get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes ORDER BY nome")
        clientes = cursor.fetchall()
        cursor.close()
        conn.close()

        return clientes
    except Exception as e:
        print(f"Erro ao buscar clientes: {e}")
        if conn:
            conn.close()
        return []
    
        

def obter_cliente(id_cliente):
    """Obtém um cliente específico por ID"""
    conn = inicia_bd()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
        cliente = cursor.fetchone()
        return cliente
    finally:
        conn.close()

def adicionar_cliente(nome, cpf, telefone, email, endereco):
    """Adiciona um novo cliente"""
    # Validação dos campos obrigatórios
    if not nome or not cpf:
        raise ValueError("Nome e CPF são obrigatórios")
    
    # Validação de CPF (formato básico)
    cpf_limpo = cpf.replace('.', '').replace('-', '')
    if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
        raise ValueError("CPF inválido")
    
    # Validação de email
    if email and '@' not in email:
        raise ValueError("Email inválido")
    
    conn = inicia_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO clientes (nome, cpf, telefone, email, endereco)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, cpf, telefone, email, endereco))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def obter_cliente_por_email(email):
    """Obtém cliente por email para login"""
    conn = inicia_bd()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM clientes WHERE email = %s", (email,))
        return cursor.fetchone()
    finally:
        conn.close()

def verificar_senha(senha_digitada, senha_hash_banco):
    """Verifica senha do cliente (se coluna existir)."""
    if not senha_hash_banco:
        return False
    return bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_hash_banco.encode('utf-8'))

def adicionar_cliente_com_senha(nome, cpf, telefone, email, endereco, senha, username=None):
    """Adiciona um cliente com credenciais de acesso."""
    if not nome or not cpf or not email or not senha:
        raise ValueError("Nome, CPF, email e senha são obrigatórios")
    cpf_limpo = cpf.replace('.', '').replace('-', '')
    if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
        raise ValueError("CPF inválido")
    if '@' not in email:
        raise ValueError("Email inválido")

    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    conn = inicia_bd()
    cursor = conn.cursor()
    try:
        # Tenta inserir incluindo colunas opcionais (username, senha_hash)
        cursor.execute(
            """
            INSERT INTO clientes (nome, cpf, telefone, email, endereco, senha_hash, username)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (nome, cpf, telefone, email, endereco, senha_hash, username)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        # Caso a tabela ainda não tenha as colunas, sinaliza claramente
        raise e
    finally:
        conn.close()

def atualizar_perfil_cliente(id_cliente, username, nome, email, cpf, telefone, endereco):
    """Atualiza dados do perfil do cliente."""
    if not nome or not email or not cpf:
        raise ValueError("Nome, email e CPF são obrigatórios")
    cpf_limpo = cpf.replace('.', '').replace('-', '')
    if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
        raise ValueError("CPF inválido")
    if '@' not in email:
        raise ValueError("Email inválido")

    conn = inicia_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE clientes
            SET username=%s, nome=%s, email=%s, cpf=%s, telefone=%s, endereco=%s
            WHERE id_cliente=%s
            """,
            (username, nome, email, cpf, telefone, endereco, id_cliente)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def atualizar_senha_cliente(id_cliente, nova_senha):
    """Atualiza a senha do cliente."""
    if len(nova_senha) < 6:
        raise ValueError("A senha deve ter pelo menos 6 caracteres")
    senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
    conn = inicia_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE clientes SET senha_hash=%s WHERE id_cliente=%s", (senha_hash, id_cliente))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def atualizar_cliente(id_cliente, nome, cpf, telefone, email, endereco):
    """Atualiza um cliente"""
    # Validação dos campos obrigatórios
    if not nome or not cpf:
        raise ValueError("Nome e CPF são obrigatórios")
    
    # Validação de CPF
    cpf_limpo = cpf.replace('.', '').replace('-', '')
    if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
        raise ValueError("CPF inválido")
    
    # Validação de email
    if email and '@' not in email:
        raise ValueError("Email inválido")
    
    conn = inicia_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE clientes 
            SET nome=%s, cpf=%s, telefone=%s, email=%s, endereco=%s
            WHERE id_cliente=%s
        """, (nome, cpf, telefone, email, endereco, id_cliente))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def excluir_cliente(id_cliente):
    """Exclui um cliente"""
    conn = inicia_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (id_cliente,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def cliente_ja_tem_vendas(id_cliente):
    """Verifica se cliente tem vendas associadas"""
    conn = inicia_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) as total FROM vendas WHERE id_cliente=%s", (id_cliente,))
        result = cursor.fetchone()
        return result[0] > 0
    finally:
        conn.close()