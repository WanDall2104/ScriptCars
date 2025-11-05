from flask import render_template, request, redirect, url_for, flash, session
from models import cliente_model
import mysql.connector

def configure_routes(app):
    def login_required(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash("Você precisa fazer login para acessar esta página", "error")
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper

    def cliente_required(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session or session.get('user_tipo') != 'cliente':
                flash("Você precisa estar logado como cliente para acessar esta página", "error")
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper

    def funcionario_required(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash("Você precisa fazer login para acessar esta página", "error")
                return redirect(url_for('login'))
            if session.get('user_tipo') != 'funcionario':
                flash("Acesso restrito aos funcionários", "error")
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper

    @app.route('/clientes')
    @funcionario_required
    def listar_clientes():
        """Lista todos os clientes"""
        clientes = cliente_model.listar_clientes()
        return render_template('clientes.html', clientes=clientes)

    @app.route('/perfil')
    @cliente_required
    def perfil_cliente():
        cliente = cliente_model.obter_cliente(session['user_id'])
        return render_template('perfil.html', cliente=cliente)

    @app.route('/perfil', methods=['POST'])
    @cliente_required
    def atualizar_perfil_cliente():
        try:
            username = request.form.get('username', '').strip() or None
            nome = request.form.get('nome', '').strip()
            email = request.form.get('email', '').strip()
            cpf = request.form.get('cpf', '').strip()
            telefone = request.form.get('telefone', '').strip()
            endereco = request.form.get('endereco', '').strip()
            cliente_model.atualizar_perfil_cliente(session['user_id'], username, nome, email, cpf, telefone, endereco)
            session['user_nome'] = username or nome
            flash("Perfil atualizado com sucesso!", "success")
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            flash(f"Erro ao atualizar perfil: {str(e)}", "error")
        return redirect(url_for('perfil_cliente'))

    @app.route('/perfil/senha', methods=['POST'])
    @cliente_required
    def atualizar_senha_cliente():
        try:
            senha_atual = request.form.get('senha_atual', '')
            nova_senha = request.form.get('nova_senha', '')
            confirmar = request.form.get('confirmar_nova', '')
            if nova_senha != confirmar:
                flash("As senhas não coincidem!", "error")
                return redirect(url_for('perfil_cliente'))
            # valida senha atual
            cliente = cliente_model.obter_cliente(session['user_id'])
            if not cliente_model.verificar_senha(senha_atual, cliente.get('senha_hash')):
                flash("Senha atual incorreta!", "error")
                return redirect(url_for('perfil_cliente'))
            cliente_model.atualizar_senha_cliente(session['user_id'], nova_senha)
            flash("Senha atualizada com sucesso!", "success")
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            flash(f"Erro ao alterar senha: {str(e)}", "error")
        return redirect(url_for('perfil_cliente'))

    @app.route('/perfil/excluir', methods=['POST'])
    @cliente_required
    def excluir_minha_conta():
        try:
            # Segurança: exige confirmação textual
            confirmacao = request.form.get('confirmacao', '')
            if confirmacao.strip().lower() != 'excluir':
                flash("Digite 'excluir' para confirmar a exclusão.", "error")
                return redirect(url_for('perfil_cliente'))
            # Verifica se cliente tem vendas
            if cliente_model.cliente_ja_tem_vendas(session['user_id']):
                flash("Não é possível excluir conta com vendas realizadas.", "error")
                return redirect(url_for('perfil_cliente'))
            cliente_model.excluir_cliente(session['user_id'])
            session.clear()
            flash("Sua conta foi excluída.", "success")
            return redirect(url_for('home'))
        except Exception as e:
            flash(f"Erro ao excluir conta: {str(e)}", "error")
            return redirect(url_for('perfil_cliente'))

    @app.route('/cliente/novo')
    @funcionario_required
    def formulario_novo_cliente():
        """Exibe formulário para novo cliente"""
        return render_template('form_cliente.html', cliente=None)

    @app.route('/cliente/novo', methods=['POST'])
    @funcionario_required
    def novo_cliente():
        """Cria um novo cliente"""
        try:
            nome = request.form['nome'].strip()
            cpf = request.form['cpf'].strip()
            telefone = request.form.get('telefone', '').strip()
            email = request.form.get('email', '').strip()
            endereco = request.form.get('endereco', '').strip()
            
            # Validações básicas
            if not nome or not cpf:
                flash("Nome e CPF são obrigatórios!", "error")
                return redirect(url_for('formulario_novo_cliente'))
            
            cliente_model.adicionar_cliente(nome, cpf, telefone, email, endereco)
            flash("Cliente cadastrado com sucesso!", "success")
            return redirect(url_for('listar_clientes'))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('formulario_novo_cliente'))
        except mysql.connector.Error as e:
            # Tratamento amigável para CPF duplicado
            if getattr(e, 'errno', None) == 1062:
                flash("Este CPF já está cadastrado. Verifique os dados do cliente.", "error")
            else:
                flash(f"Erro ao cadastrar cliente: {str(e)}", "error")
            return redirect(url_for('formulario_novo_cliente'))
        except Exception as e:
            # Verifica se é erro de CPF duplicado mesmo sendo Exception genérica
            error_msg = str(e)
            if "1062" in error_msg or "Duplicate entry" in error_msg or "uq_clientes_cpf" in error_msg:
                flash("Este CPF já está cadastrado. Verifique os dados do cliente.", "error")
            else:
                flash(f"Erro ao cadastrar cliente: {error_msg}", "error")
            return redirect(url_for('formulario_novo_cliente'))

    @app.route('/cliente/editar/<int:id>')
    @funcionario_required
    def formulario_editar_cliente(id):
        """Exibe formulário para editar cliente"""
        cliente = cliente_model.obter_cliente(id)
        if not cliente:
            flash("Cliente não encontrado!", "error")
            return redirect(url_for('listar_clientes'))
        
        return render_template('form_cliente.html', cliente=cliente)

    @app.route('/cliente/editar/<int:id>', methods=['POST'])
    @funcionario_required
    def editar_cliente(id):
        """Atualiza um cliente"""
        try:
            nome = request.form['nome'].strip()
            cpf = request.form['cpf'].strip()
            telefone = request.form.get('telefone', '').strip()
            email = request.form.get('email', '').strip()
            endereco = request.form.get('endereco', '').strip()
            
            # Validações básicas
            if not nome or not cpf:
                flash("Nome e CPF são obrigatórios!", "error")
                return redirect(url_for('formulario_editar_cliente', id=id))
            
            cliente_model.atualizar_cliente(id, nome, cpf, telefone, email, endereco)
            flash("Cliente atualizado com sucesso!", "success")
            return redirect(url_for('listar_clientes'))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('formulario_editar_cliente', id=id))
        except mysql.connector.Error as e:
            if getattr(e, 'errno', None) == 1062:
                flash("Já existe um cliente com este CPF. Atualize o CPF ou verifique duplicidade.", "error")
            else:
                flash(f"Erro ao atualizar cliente: {str(e)}", "error")
            return redirect(url_for('formulario_editar_cliente', id=id))
        except Exception as e:
            # Verifica se é erro de CPF duplicado mesmo sendo Exception genérica
            error_msg = str(e)
            if "1062" in error_msg or "Duplicate entry" in error_msg or "uq_clientes_cpf" in error_msg:
                flash("Já existe um cliente com este CPF. Atualize o CPF ou verifique duplicidade.", "error")
            else:
                flash(f"Erro ao atualizar cliente: {error_msg}", "error")
            return redirect(url_for('formulario_editar_cliente', id=id))

    @app.route('/cliente/excluir/<int:id>')
    @funcionario_required
    def excluir_cliente(id):
        """Exclui um cliente"""
        try:
            # Verifica se cliente tem vendas
            if cliente_model.cliente_ja_tem_vendas(id):
                flash("Não é possível excluir cliente que já possui vendas associadas!", "error")
                return redirect(url_for('listar_clientes'))
            
            cliente_model.excluir_cliente(id)
            flash("Cliente excluído com sucesso!", "success")
        except Exception as e:
            flash(f"Erro ao excluir cliente: {str(e)}", "error")
        
        return redirect(url_for('listar_clientes'))