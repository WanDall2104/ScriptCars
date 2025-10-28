from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import venda_model, cliente_model, veiculo_model, funcionario_model

venda_bp = Blueprint('venda', __name__)

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Você precisa fazer login para acessar esta página", "error")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@venda_bp.route('/vendas')
@login_required
def listar_vendas():
    """Lista todas as vendas"""
    vendas = venda_model.listar_vendas()
    return render_template('vendas.html', vendas=vendas)

@venda_bp.route('/venda/nova')
@login_required
def formulario_nova_venda():
    """Exibe formulário para nova venda"""
    clientes = cliente_model.listar_clientes()
    veiculos = veiculo_model.listar_veiculos_disponiveis()
    funcionarios = funcionario_model.listar_funcionarios()
    
    # Obtém ID do funcionário logado
    funcionario_logado_id = session.get('user_id')
    
    return render_template('form_venda.html', 
                         clientes=clientes, 
                         veiculos=veiculos, 
                         funcionarios=funcionarios,
                         funcionario_logado_id=funcionario_logado_id)

@venda_bp.route('/venda/nova', methods=['POST'])
@login_required
def nova_venda():
    """Registra uma nova venda"""
    try:
        id_cliente = request.form['id_cliente']
        id_veiculo = request.form['id_veiculo']
        id_funcionario = request.form.get('id_funcionario', session.get('user_id'))
        valor_final = request.form['valor_final']
        forma_pagamento = request.form.get('forma_pagamento', '').strip()
        observacoes = request.form.get('observacoes', '').strip()
        
        # Validações
        if not id_cliente or not id_veiculo or not valor_final:
            flash("Todos os campos são obrigatórios!", "error")
            return redirect(url_for('venda.formulario_nova_venda'))
        
        # Registra a venda
        venda_model.adicionar_venda(id_cliente, id_veiculo, id_funcionario, valor_final, forma_pagamento, observacoes)
        flash("Venda registrada com sucesso!", "success")
        return redirect(url_for('venda.listar_vendas'))
    
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for('venda.formulario_nova_venda'))
    except Exception as e:
        flash(f"Erro ao registrar venda: {str(e)}", "error")
        return redirect(url_for('venda.formulario_nova_venda'))

@venda_bp.route('/venda/excluir/<int:id>')
@login_required
def excluir_venda(id):
    """Exclui uma venda"""
    try:
        venda_model.excluir_venda(id)
        flash("Venda excluída com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao excluir venda: {str(e)}", "error")
    
    return redirect(url_for('venda.listar_vendas'))

@venda_bp.route('/venda/detalhes/<int:id>')
@login_required
def detalhes_venda(id):
    """Exibe detalhes de uma venda"""
    venda = venda_model.obter_venda(id)
    if not venda:
        flash("Venda não encontrada!", "error")
        return redirect(url_for('venda.listar_vendas'))
    
    return render_template('detalhes_venda.html', venda=venda)