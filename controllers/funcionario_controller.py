from flask import render_template, request, redirect, url_for, flash, session
from models import funcionario_model

def configure_routes(app):
    # Decorator para verificar se usuário está logado
    def login_required(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash("Você precisa fazer login para acessar esta página", "error")
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper

    # Decorator para restringir a funcionários
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

    @app.route('/funcionarios')
    @funcionario_required
    def listar_funcionarios():
        """Lista todos os funcionários"""
        funcionarios = funcionario_model.listar_funcionarios()
        return render_template('funcionarios.html', funcionarios=funcionarios)

    @app.route('/funcionario/novo')
    @funcionario_required
    def formulario_novo_funcionario():
        """Exibe formulário para novo funcionário"""
        return render_template('form_funcionario.html', funcionario=None)

    @app.route('/funcionario/novo', methods=['POST'])
    @funcionario_required
    def novo_funcionario():
        """Cria um novo funcionário"""
        try:
            nome = request.form['nome'].strip()
            email = request.form['email'].strip()
            senha = request.form['senha']
            cargo = request.form['cargo'].strip()
            
            # Validações
            if not nome or not email or not senha or not cargo:
                flash("Todos os campos são obrigatórios!", "error")
                return redirect(url_for('formulario_novo_funcionario'))
            
            # Validação de senha
            if len(senha) < 6:
                flash("A senha deve ter pelo menos 6 caracteres!", "error")
                return redirect(url_for('formulario_novo_funcionario'))
            
            funcionario_model.adicionar_funcionario(nome, email, senha, cargo)
            flash("Funcionário cadastrado com sucesso!", "success")
            return redirect(url_for('listar_funcionarios'))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('formulario_novo_funcionario'))
        except Exception as e:
            flash(f"Erro ao cadastrar funcionário: {str(e)}", "error")
            return redirect(url_for('formulario_novo_funcionario'))

    @app.route('/funcionario/editar/<int:id>')
    @funcionario_required
    def formulario_editar_funcionario(id):
        """Exibe formulário para editar funcionário"""
        funcionario = funcionario_model.obter_funcionario(id)
        if not funcionario:
            flash("Funcionário não encontrado!", "error")
            return redirect(url_for('listar_funcionarios'))
        
        # Remove senha do objeto
        if 'senha_hash' in funcionario:
            del funcionario['senha_hash']
        
        return render_template('form_funcionario.html', funcionario=funcionario)

    @app.route('/funcionario/editar/<int:id>', methods=['POST'])
    @funcionario_required
    def editar_funcionario(id):
        """Atualiza um funcionário"""
        try:
            nome = request.form['nome'].strip()
            email = request.form['email'].strip()
            cargo = request.form['cargo'].strip()
            senha = request.form.get('senha', '').strip()
            
            # Validações
            if not nome or not email or not cargo:
                flash("Todos os campos são obrigatórios!", "error")
                return redirect(url_for('formulario_editar_funcionario', id=id))
            
            # Se informou nova senha, valida
            if senha and len(senha) < 6:
                flash("A senha deve ter pelo menos 6 caracteres!", "error")
                return redirect(url_for('formulario_editar_funcionario', id=id))
            
            # Atualiza com ou sem nova senha
            if senha:
                funcionario_model.atualizar_funcionario(id, nome, email, cargo, senha)
            else:
                funcionario_model.atualizar_funcionario(id, nome, email, cargo)
            
            flash("Funcionário atualizado com sucesso!", "success")
            return redirect(url_for('listar_funcionarios'))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('formulario_editar_funcionario', id=id))
        except Exception as e:
            flash(f"Erro ao atualizar funcionário: {str(e)}", "error")
            return redirect(url_for('formulario_editar_funcionario', id=id))

    @app.route('/funcionario/excluir/<int:id>')
    @funcionario_required
    def excluir_funcionario(id):
        """Exclui um funcionário"""
        try:
            # Impede exclusão se houver vendas vinculadas
            if funcionario_model.funcionario_tem_vendas(id):
                flash("Não é possível excluir: o funcionário possui vendas vinculadas.", "error")
                return redirect(url_for('listar_funcionarios'))
            funcionario_model.excluir_funcionario(id)
            flash("Funcionário excluído com sucesso!", "success")
        except Exception as e:
            flash(f"Erro ao excluir funcionário: {str(e)}", "error")
        
        return redirect(url_for('listar_funcionarios'))