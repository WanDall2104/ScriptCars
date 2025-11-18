from flask import render_template, request, redirect, url_for, flash, session, make_response
from models import funcionario_model, cliente_model
from datetime import timedelta
import mysql.connector
from config import Config


def configure_routes(app):
    @app.route('/login')
    def login():
        """Exibe página de login"""
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def fazer_login():
        """Processa o login"""
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        lembrar = request.form.get('lembrar') == 'on'
        
        # Validações
        if not email or not senha:
            flash("Email e senha são obrigatórios!", "error")
            return redirect(url_for('login'))
        
        try:
            # 1) Tenta logar como cliente (padrão para público)
            cliente = cliente_model.obter_cliente_por_email(email)
            if cliente and cliente.get('senha_hash') and cliente_model.verificar_senha(senha, cliente['senha_hash']):
                session['user_id'] = cliente['id_cliente']
                session['user_nome'] = cliente.get('username') or cliente['nome']
                session['user_email'] = cliente['email']
                session['user_tipo'] = 'cliente'
            else:
                # 2) Fallback: tenta logar como funcionário (para área administrativa)
                funcionario = funcionario_model.obter_funcionario_por_email(email)
                if not funcionario or not funcionario_model.verificar_senha(senha, funcionario['senha_hash']):
                    flash("Email ou senha inválidos!", "error")
                    return redirect(url_for('login'))
                session['user_id'] = funcionario['id_funcionario']
                session['user_nome'] = funcionario['nome']
                session['user_email'] = funcionario['email']
                session['user_cargo'] = funcionario['cargo']
                session['user_tipo'] = 'funcionario'
            
            # Se o usuário pediu para lembrar, define cookie
            if lembrar:
                session.permanent = True
                session.permanent_session_lifetime = timedelta(days=30)
            
            flash(f"Bem-vindo, {session['user_nome']}!", "success")
            return redirect(url_for('home'))
        
        except Exception as e:
            flash(f"Erro ao fazer login: {str(e)}", "error")
            return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        """Realiza logout"""
        if 'user_id' in session:
            nome = session.get('user_nome', 'Usuário')
            session.clear()
            flash(f"Até logo, {nome}!", "info")
        return redirect(url_for('home'))

    @app.route('/cadastro')
    def cadastro():
        """Exibe página de cadastro"""
        return render_template('cadastro.html')

    @app.route('/cadastro', methods=['POST'])
    def fazer_cadastro():
        """Processa o cadastro de novo cliente (padrão público)."""
        username = request.form.get('username', '').strip() or None
        nome = request.form.get('nome', '').strip()
        cpf = request.form.get('cpf', '').strip()
        telefone = request.form.get('telefone', '').strip()
        email = request.form.get('email', '').strip()
        endereco = request.form.get('endereco', '').strip()
        senha = request.form.get('senha', '')
        confirmar_senha = request.form.get('confirmar_senha', '')

        # Validações
        if not nome or not email or not senha or not cpf:
            flash("Nome, email, senha e CPF são obrigatórios!", "error")
            return redirect(url_for('cadastro'))

        if len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres!", "error")
            return redirect(url_for('cadastro'))

        if senha != confirmar_senha:
            flash("As senhas não coincidem!", "error")
            return redirect(url_for('cadastro'))

        try:
            cliente_model.adicionar_cliente_com_senha(nome, cpf, telefone, email, endereco, senha, username)
            flash("Cadastro realizado com sucesso! Faça login para continuar.", "success")
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('cadastro'))
        except mysql.connector.Error as e:
            # Tratamento amigável para CPF duplicado
            if getattr(e, 'errno', None) == 1062:
                flash("Este CPF já está cadastrado. Verifique os dados ou faça login com sua conta existente.", "error")
            else:
                flash(f"Erro ao cadastrar: {str(e)}", "error")
            return redirect(url_for('cadastro'))
        except Exception as e:
            # Verifica se é erro de CPF duplicado mesmo sendo Exception genérica
            error_msg = str(e)
            if "1062" in error_msg or "Duplicate entry" in error_msg or "uq_clientes_cpf" in error_msg:
                flash("Este CPF já está cadastrado. Verifique os dados ou faça login com sua conta existente.", "error")
            else:
                flash(f"Erro ao cadastrar: {error_msg}", "error")
            return redirect(url_for('cadastro'))
