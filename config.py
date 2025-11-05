import mysql.connector


class Config:
    # Chave de sessão e credenciais do banco no mesmo padrão das aulas
    SECRET_KEY = 'chave_super_segura_para_sessao_2024'
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'admin',
        'database': 'concessionaria'
    }
    # Opções de sessão (equivalente ao que estava em app.py)
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = 2592000  # 30 dias em segundos


def get_db_connection():
    # Mantido por compatibilidade, usando Config.DB_CONFIG
    return mysql.connector.connect(**Config.DB_CONFIG)
