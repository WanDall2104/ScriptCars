import mysql.connector
import os
from datetime import datetime

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
        import mysql.connector
        try:
            connection = mysql.connector.connect(**Config.DB_CONFIG)
            return connection
        except mysql.connector.Error as err:
            print(f"Erro ao se conectar com o banco de dados: {err}")
            return None
    
