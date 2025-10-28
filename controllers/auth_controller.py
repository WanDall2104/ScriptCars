from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from models import funcionario_model
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    """Exibe página de login"""
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def fazer_login():
    """Processa o login"""
    email = request.form.get('email', '').strip()
    senha = request.form.get('senha', '')
    lembrar = request.form.get('lembrar') == 'on'
    
    # Validações
    if not email or not senha:
        flash("Email e senha são obrigatórios!", "error")
        return redirect(url_for('auth.login'))
    
    try:
        # Busca funcionário no banco
        funcionario = funcionario_model.obter_funcionario_por_email(email)
        
        if not funcionario:
            flash("Email ou senha inválidos!", "error")
            return redirect(url_for('auth.login'))
        
        # Verifica senha
        if not funcionario_model.verificar_senha(senha, funcionario['senha_hash']):
            flash("Email ou senha inválidos!", "error")
            return redirect(url_for('auth.login'))
        
        # Cria sessão
        session['user_id'] = funcionario['id_funcionario']
        session['user_nome'] = funcionario['nome']
        session['user_email'] = funcionario['email']
        session['user_cargo'] = funcionario['cargo']
        
        # Se o usuário pediu para lembrar, define cookie
        if lembrar:
            session.permanent = True
            session.permanent_session_lifetime = timedelta(days=30)
        
        flash(f"Bem-vindo, {funcionario['nome']}!", "success")
        return redirect(url_for('home'))
    
    except Exception as e:
        flash(f"Erro ao fazer login: {str(e)}", "error")
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    """Realiza logout"""
    if 'user_id' in session:
        nome = session.get('user_nome', 'Usuário')
        session.clear()
        flash(f"Até logo, {nome}!", "info")
    return redirect(url_for('home'))

@auth_bp.route('/cadastro')
def cadastro():
    """Exibe página de cadastro"""
    return render_template('cadastro.html')

@auth_bp.route('/cadastro', methods=['POST'])
def fazer_cadastro():
    """Processa o cadastro de novo funcionário"""
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()
    senha = request.form.get('senha', '')
    confirmar_senha = request.form.get('confirmar_senha', '')
    cargo = request.form.get('cargo', '').strip()
    
    # Validações
    if not nome or not email or not senha or not cargo:
        flash("Todos os campos são obrigatórios!", "error")
        return redirect(url_for('auth.cadastro'))
    
    if len(senha) < 6:
        flash("A senha deve ter pelo menos 6 caracteres!", "error")
        return redirect(url_for('auth.cadastro'))
    
    if senha != confirmar_senha:
        flash("As senhas não coincidem!", "error")
        return redirect(url_for('auth.cadastro'))
    
    try:
        funcionario_model.adicionar_funcionario(nome, email, senha, cargo)
        flash("Cadastro realizado com sucesso! Faça login para continuar.", "success")
        return redirect(url_for('auth.login'))
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for('auth.cadastro'))
    except Exception as e:
        flash(f"Erro ao cadastrar: {str(e)}", "error")
        return redirect(url_for('auth.cadastro'))
