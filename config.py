import mysql.connector

def inicia_bd():
    """Inicia conexão com o banco de dados"""
    try:
        return mysql.connector.connect(**Config.DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Erro de conexão com o BD: {err}")
        return None

class Config:
    # Chave de sessão e credenciais do banco no mesmo padrão das aulas
    SECRET_KEY = 'chave_super_segura_para_sessao_2024'
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'concessionaria'
    }
    # Opções de sessão (equivalente ao que estava em app.py)
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = 2592000  # 30 dias em segundos

def get_db_connection():
    # Mantido por compatibilidade, usando Config.DB_CONFIG
    return mysql.connector.connect(**Config.DB_CONFIG)
