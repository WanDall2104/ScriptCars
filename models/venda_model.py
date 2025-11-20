from config import Config

def listar_vendas():
    """Lista todas as vendas com informações relacionadas"""
    conn = Config.get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.id_venda, v.data_venda, v.valor_final, v.forma_pagamento, v.observacoes,
                   c.nome AS nome_cliente, c.cpf AS cpf_cliente,
                   ve.marca, ve.modelo, ve.ano AS ano_veiculo,
                   f.nome AS nome_funcionario, f.cargo
            FROM vendas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            JOIN veiculos ve ON v.id_veiculo = ve.id_veiculo
            JOIN funcionarios f ON v.id_funcionario = f.id_funcionario
            ORDER BY v.data_venda DESC
        """)
        vendas = cursor.fetchall()
        cursor.close()
        conn.close()
        return vendas
    
    except Exception as e:
        print(f"Erro ao listar vendas: {e}")
        if conn:
            conn.close()
        return []

def obter_venda(id_venda):
    """Obtém uma venda específica por ID"""
    conn = Config.get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.*, c.nome AS nome_cliente, ve.modelo AS modelo_veiculo, f.nome AS nome_funcionario
            FROM vendas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            JOIN veiculos ve ON v.id_veiculo = ve.id_veiculo
            JOIN funcionarios f ON v.id_funcionario = f.id_funcionario
            WHERE v.id_venda = %s
        """, (id_venda,))
        venda = cursor.fetchone()
        cursor.close()
        conn.close()
        return venda
    
    except Exception as e:
        print(f"Erro ao obter venda: {e}")
        if conn:
            conn.close()
        return None

def adicionar_venda(id_cliente, id_veiculo, id_funcionario, valor_final, forma_pagamento=None, observacoes=None):
    """Adiciona uma nova venda e marca o veículo como indisponível"""
    # Validação dos campos obrigatórios
    if not id_cliente or not id_veiculo or not id_funcionario or not valor_final:
        raise ValueError("Todos os campos são obrigatórios")
    
    # Validação de valor
    try:
        valor_float = float(valor_final)
        if valor_float <= 0:
            raise ValueError("Valor deve ser maior que zero")
    except ValueError:
        raise ValueError("Valor inválido")
    
    conn = Config.get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        # Verifica se veículo está disponível
        cursor.execute("SELECT disponivel FROM veiculos WHERE id_veiculo=%s", (id_veiculo,))
        result = cursor.fetchone()
        if not result or not result[0]:
            raise ValueError("Veículo não está disponível")
        
        # Insere a venda
        cursor.execute("""
            INSERT INTO vendas (id_cliente, id_veiculo, id_funcionario, valor_final, forma_pagamento, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_cliente, id_veiculo, id_funcionario, valor_final, forma_pagamento, observacoes))
        
        # Marca o veículo como indisponível
        cursor.execute("UPDATE veiculos SET disponivel=FALSE WHERE id_veiculo=%s", (id_veiculo,))
        
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def atualizar_venda(id_venda, id_cliente, id_veiculo, id_funcionario, valor_final, forma_pagamento=None, observacoes=None):
    """Atualiza uma venda existente"""
    # Validação dos campos obrigatórios
    if not id_cliente or not id_veiculo or not id_funcionario or not valor_final:
        raise ValueError("Todos os campos são obrigatórios")
    
    # Validação de valor
    try:
        valor_float = float(valor_final)
        if valor_float <= 0:
            raise ValueError("Valor deve ser maior que zero")
    except ValueError:
        raise ValueError("Valor inválido")
    
    conn = Config.get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        # Obtém o veículo atual da venda
        cursor.execute("SELECT id_veiculo FROM vendas WHERE id_venda=%s", (id_venda,))
        venda_atual = cursor.fetchone()
        
        if not venda_atual:
            raise ValueError("Venda não encontrada")
        
        veiculo_antigo_id = venda_atual[0]
        
        # Se o veículo mudou, precisa liberar o antigo e reservar o novo
        if veiculo_antigo_id != int(id_veiculo):
            # Libera o veículo antigo
            cursor.execute("UPDATE veiculos SET disponivel=TRUE WHERE id_veiculo=%s", (veiculo_antigo_id,))
            
            # Verifica se o novo veículo está disponível
            cursor.execute("SELECT disponivel FROM veiculos WHERE id_veiculo=%s", (id_veiculo,))
            result = cursor.fetchone()
            if not result or not result[0]:
                conn.rollback()
                raise ValueError("Veículo não está disponível")
            
            # Reserva o novo veículo
            cursor.execute("UPDATE veiculos SET disponivel=FALSE WHERE id_veiculo=%s", (id_veiculo,))
        
        # Atualiza a venda
        cursor.execute("""
            UPDATE vendas 
            SET id_cliente=%s, id_veiculo=%s, id_funcionario=%s, valor_final=%s, 
                forma_pagamento=%s, observacoes=%s
            WHERE id_venda=%s
        """, (id_cliente, id_veiculo, id_funcionario, valor_final, forma_pagamento, observacoes, id_venda))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def excluir_venda(id_venda):
    """Exclui uma venda e marca o veículo como disponível novamente"""
    conn = Config.get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        # Obtém o ID do veículo antes de excluir
        cursor.execute("SELECT id_veiculo FROM vendas WHERE id_venda=%s", (id_venda,))
        result = cursor.fetchone()
        
        if result:
            id_veiculo = result[0]
            # Exclui a venda
            cursor.execute("DELETE FROM vendas WHERE id_venda=%s", (id_venda,))
            # Marca o veículo como disponível novamente
            cursor.execute("UPDATE veiculos SET disponivel=TRUE WHERE id_veiculo=%s", (id_veiculo,))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def obter_relatorio_vendas(data_inicio=None, data_fim=None):
    """Gera relatório de vendas no período especificado"""
    conn = Config.get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        if data_inicio and data_fim:
            cursor.execute("""
                SELECT COUNT(*) as total_vendas, SUM(valor_final) as total_valor
                FROM vendas
                WHERE data_venda BETWEEN %s AND %s
            """, (data_inicio, data_fim))
        elif data_inicio:
            cursor.execute("""
                SELECT COUNT(*) as total_vendas, SUM(valor_final) as total_valor
                FROM vendas
                WHERE data_venda >= %s
            """, (data_inicio,))
        else:
            cursor.execute("""
                SELECT COUNT(*) as total_vendas, SUM(valor_final) as total_valor
                FROM vendas
            """)
        
        relatorio = cursor.fetchone()
        cursor.close()
        conn.close()
        return relatorio
    
    except Exception as e:
        print(f"Erro ao obter relatório de vendas: {e}")
        if conn:
            conn.close()
        return None