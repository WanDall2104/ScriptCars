import bcrypt
from config import Config

def listar_funcionarios():
    """Lista todos os funcionários"""
    conn = Config.get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_funcionario, nome, email, cargo, data_admissao FROM funcionarios ORDER BY nome")
        funcionarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return funcionarios
    
    except Exception as e:
        print(f"Erro ao listar funcionários: {e}")
        if conn:
            conn.close()
        return []

def obter_funcionario(id_funcionario):
    """Obtém um funcionário específico por ID"""
    conn = Config.get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM funcionarios WHERE id_funcionario = %s", (id_funcionario,))
        funcionario = cursor.fetchone()
        cursor.close()
        conn.close()
        return funcionario
    
    except Exception as e:
        print(f"Erro ao obter funcionário: {e}")
        if conn:
            conn.close()
        return None

def obter_funcionario_por_email(email):
    """Obtém funcionário por email para login"""
    conn = Config.get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM funcionarios WHERE email = %s", (email,))
        funcionario = cursor.fetchone()
        cursor.close()
        conn.close()
        return funcionario
    
    except Exception as e:
        print(f"Erro ao obter funcionário por email: {e}")
        if conn:
            conn.close()
        return None

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
    
    conn = Config.get_db_connection()
    if not conn:
        return None
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
        cursor.close()
        conn.close()

def atualizar_funcionario(id_funcionario, nome, email, cargo, senha=None):
    """Atualiza um funcionário"""
    # Validação dos campos obrigatórios
    if not nome or not email or not cargo:
        raise ValueError("Todos os campos são obrigatórios")
    
    conn = Config.get_db_connection()
    if not conn:
        return None
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
        cursor.close()
        conn.close()

def excluir_funcionario(id_funcionario):
    """Exclui um funcionário"""
    conn = Config.get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM funcionarios WHERE id_funcionario = %s", (id_funcionario,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def funcionario_tem_vendas(id_funcionario: int) -> bool:
    """Retorna True se o funcionário possui vendas vinculadas."""
    conn = Config.get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM vendas WHERE id_funcionario=%s", (id_funcionario,))
        total = cursor.fetchone()[0]
        return total > 0
    except Exception as e:
        print(f"Erro ao verificar vendas do funcionário: {e}")
        return False
    finally:
        cursor.close()
        conn.close()