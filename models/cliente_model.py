from config import get_db_connection

def listar_clientes():
    """Lista todos os clientes"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM clientes ORDER BY nome")
        clientes = cursor.fetchall()
        return clientes
    finally:
        conn.close()

def obter_cliente(id_cliente):
    """Obtém um cliente específico por ID"""
    conn = get_db_connection()
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
    
    conn = get_db_connection()
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
    
    conn = get_db_connection()
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
    conn = get_db_connection()
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
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) as total FROM vendas WHERE id_cliente=%s", (id_cliente,))
        result = cursor.fetchone()
        return result[0] > 0
    finally:
        conn.close()