from flask import Flask, render_template, session
from controllers.auth_controller import auth_bp
from controllers.funcionario_controller import funcionario_bp
from controllers.cliente_controller import cliente_bp
from controllers.veiculo_controller import veiculo_bp
from controllers.venda_controller import venda_bp

app = Flask(__name__, 
            template_folder='views/templates',
            static_folder='views/static')
app.secret_key = 'chave_super_segura_para_sessao_2024'  # Chave secreta para sessões
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 2592000  # 30 dias em segundos

# Registro de Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(funcionario_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(veiculo_bp)
app.register_blueprint(venda_bp)

# ========== PÁGINAS PÚBLICAS ==========

# Filtro de formatação monetária BRL para templates Jinja
@app.template_filter('moeda_brl')
def moeda_brl(valor):
    """Formata número no padrão monetário brasileiro, ex: 12345.6 -> R$ 12.345,60"""
    try:
        numero = float(valor) if valor is not None else 0.0
        # Usa separador de milhar com vírgula, depois troca pontuação para padrão BR
        formatado = f"{numero:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"R$ {formatado}"
    except Exception:
        return f"R$ {valor}"

@app.route('/')
def home():
    """Página inicial pública"""
    return render_template('home.html', logged_in='user_id' in session)

@app.route('/sobre')
def sobre():
    """Página sobre a concessionária (pública)"""
    return render_template('sobre.html', logged_in='user_id' in session)

@app.route('/veiculos_publicos')
def veiculos_publicos():
    """Página de veículos disponíveis (pública)"""
    from models import veiculo_model
    veiculos = veiculo_model.listar_veiculos_disponiveis()
    return render_template('veiculos_disponiveis.html', veiculos=veiculos, logged_in='user_id' in session)


# ========== CONTEXTO GLOBAL ==========

@app.context_processor
def injetar_usuario():
    """Injeta informações do usuário em todas as templates"""
    return {
        'logged_in': 'user_id' in session,
        'user_nome': session.get('user_nome', ''),
        'user_cargo': session.get('user_cargo', '')
    }

@app.before_request
def proteger_rotas_admin():
    """Verifica se rotas administrativas estão protegidas"""
    from flask import request, redirect, url_for, session
    rotas_admin = ['/funcionarios', '/clientes', '/vendas']
    
    if any(request.path.startswith(rota) for rota in rotas_admin):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)