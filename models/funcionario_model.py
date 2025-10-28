from config import get_db_connection
import bcrypt

def listar_funcionarios():
    """Lista todos os funcionários"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_funcionario, nome, email, cargo, data_admissao FROM funcionarios ORDER BY nome")
        funcionarios = cursor.fetchall()
        return funcionarios
    finally:
        conn.close()

def obter_funcionario(id_funcionario):
    """Obtém um funcionário específico por ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM funcionarios WHERE id_funcionario = %s", (id_funcionario,))
        funcionario = cursor.fetchone()
        return funcionario
    finally:
        conn.close()

def obter_funcionario_por_email(email):
    """Obtém funcionário por email para login"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM funcionarios WHERE email = %s", (email,))
        funcionario = cursor.fetchone()
        return funcionario
    finally:
        conn.close()

def verificar_senha(senha_digitada, senha_hash_banco):
    """Verifica se a senha digitada corresponde ao hash"""
    return bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_hash_banco.encode('utf-8'))

def adicionar_funcionario(nome, email, senha, cargo):
    """Adiciona um novo funcionário"""
    # Validação dos campos obrigatórios
    if not nome or not email or not senha or not cargo:
        raise ValueError("Todos os campos são obrigatórios")
    
    # Validação de email
    if '@' not in email:
        raise ValueError("Email inválido")
    
    # Hash da senha
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO funcionarios (nome, email, senha_hash, cargo)
            VALUES (%s, %s, %s, %s)
        """, (nome, email, senha_hash, cargo))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def atualizar_funcionario(id_funcionario, nome, email, cargo, senha=None):
    """Atualiza um funcionário"""
    # Validação dos campos obrigatórios
    if not nome or not email or not cargo:
        raise ValueError("Todos os campos são obrigatórios")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if senha:
            # Hash da nova senha
            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("""
                UPDATE funcionarios
                SET nome=%s, email=%s, cargo=%s, senha_hash=%s
                WHERE id_funcionario=%s
            """, (nome, email, cargo, senha_hash, id_funcionario))
        else:
            cursor.execute("""
                UPDATE funcionarios
                SET nome=%s, email=%s, cargo=%s
                WHERE id_funcionario=%s
            """, (nome, email, cargo, id_funcionario))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def excluir_funcionario(id_funcionario):
    """Exclui um funcionário"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM funcionarios WHERE id_funcionario = %s", (id_funcionario,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()