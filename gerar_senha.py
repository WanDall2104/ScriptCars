"""
Script para gerar hash de senha para o administrador
"""

import bcrypt

def gerar_hash_senha(senha):
    """Gera hash bcrypt para uma senha"""
    senha_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    return hash_bytes.decode('utf-8')

if __name__ == '__main__':
    # Gera hash para a senha admin123
    senha = "admin123"
    hash_resultado = gerar_hash_senha(senha)
    
    print("=" * 60)
    print("GERADOR DE HASH DE SENHA")
    print("=" * 60)
    print(f"\nSenha: {senha}")
    print(f"Hash: {hash_resultado}")
    print("\nPara usar no banco de dados, execute:")
    print(f"UPDATE funcionarios SET senha_hash = '{hash_resultado}' WHERE email = 'admin@concessionaria.com';")
    print("\nOu execute no MySQL:")
    print(f"INSERT INTO funcionarios (nome, email, senha_hash, cargo) VALUES")
    print(f"('Admin', 'admin@concessionaria.com', '{hash_resultado}', 'Administrador');")
    print("=" * 60)
