from config import Config

def listar_veiculos():
    """Lista todos os veículos"""
    conn = Config.get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM veiculos ORDER BY marca, modelo")
        veiculos = cursor.fetchall()
        cursor.close()
        conn.close()
        return veiculos
    
    except Exception as e:
        print(f"Erro ao listar veículos: {e}")
        if conn:
            conn.close()
        return []

def listar_veiculos_disponiveis():
    """Lista apenas veículos disponíveis"""
    conn = Config.get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM veiculos WHERE disponivel=TRUE ORDER BY marca, modelo")
        veiculos = cursor.fetchall()
        cursor.close()
        conn.close()
        return veiculos
    
    except Exception as e:
        print(f"Erro ao listar veículos disponíveis: {e}")
        if conn:
            conn.close()
        return []

def obter_veiculo(id_veiculo):
    """Obtém um veículo específico por ID"""
    conn = Config.get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM veiculos WHERE id_veiculo = %s", (id_veiculo,))
        veiculo = cursor.fetchone()
        cursor.close()
        conn.close()
        return veiculo
    
    except Exception as e:
        print(f"Erro ao obter veículo: {e}")
        if conn:
            conn.close()
        return None

def adicionar_veiculo(marca, modelo, ano, preco, foto=None, km_rodados=0, cor=None, combustivel=None):
    """Adiciona um novo veículo"""
    # Validação dos campos obrigatórios
    if not marca or not modelo or not ano or not preco:
        raise ValueError("Marca, modelo, ano e preço são obrigatórios")
    
    # Validação de ano
    try:
        ano_int = int(ano)
        if ano_int < 1900 or ano_int > 2025:
            raise ValueError("Ano inválido")
    except ValueError:
        raise ValueError("Ano inválido")
    
    # Validação de preço
    try:
        preco_float = float(preco)
        if preco_float <= 0:
            raise ValueError("Preço deve ser maior que zero")
    except ValueError:
        raise ValueError("Preço inválido")
    
    conn = Config.get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO veiculos (marca, modelo, ano, preco, foto, km_rodados, cor, combustivel)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (marca, modelo, ano, preco, foto, km_rodados, cor, combustivel))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def atualizar_veiculo(id_veiculo, marca, modelo, ano, preco, disponivel=None, km_rodados=None, cor=None, combustivel=None, foto=None):
    """Atualiza um veículo"""
    # Validação dos campos obrigatórios
    if not marca or not modelo or not ano or not preco:
        raise ValueError("Marca, modelo, ano e preço são obrigatórios")
    
    # Validação de ano
    try:
        ano_int = int(ano)
        if ano_int < 1900 or ano_int > 2025:
            raise ValueError("Ano inválido")
    except ValueError:
        raise ValueError("Ano inválido")
    
    # Validação de preço
    try:
        preco_float = float(preco)
        if preco_float <= 0:
            raise ValueError("Preço deve ser maior que zero")
    except ValueError:
        raise ValueError("Preço inválido")
    
    conn = Config.get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        # Monta a query dinamicamente baseado nos campos fornecidos
        campos = []
        valores = []
        
        if marca:
            campos.append("marca=%s")
            valores.append(marca)
        if modelo:
            campos.append("modelo=%s")
            valores.append(modelo)
        if ano:
            campos.append("ano=%s")
            valores.append(ano)
        if preco:
            campos.append("preco=%s")
            valores.append(preco)
        if disponivel is not None:
            campos.append("disponivel=%s")
            valores.append(disponivel)
        if km_rodados is not None:
            campos.append("km_rodados=%s")
            valores.append(km_rodados)
        if cor:
            campos.append("cor=%s")
            valores.append(cor)
        if combustivel:
            campos.append("combustivel=%s")
            valores.append(combustivel)
        if foto:
            campos.append("foto=%s")
            valores.append(foto)
        
        valores.append(id_veiculo)
        query = f"UPDATE veiculos SET {', '.join(campos)} WHERE id_veiculo=%s"
        
        cursor.execute(query, valores)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def excluir_veiculo(id_veiculo):
    """Exclui um veículo"""
    conn = Config.get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM veiculos WHERE id_veiculo=%s", (id_veiculo,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def veiculo_tem_vendas(id_veiculo):
    """Verifica se veículo tem vendas associadas"""
    conn = Config.get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) as total FROM vendas WHERE id_veiculo=%s", (id_veiculo,))
        result = cursor.fetchone()
        return result[0] > 0
    except Exception as e:
        print(f"Erro ao verificar vendas do veículo: {e}")
        return False
    finally:
        cursor.close()
        conn.close()