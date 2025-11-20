from flask import Flask, render_template, session, request, url_for, redirect
from config import Config
from controllers import auth_controller, funcionario_controller, cliente_controller, veiculo_controller, venda_controller

app = Flask(__name__, 
            template_folder='views/templates',
            static_folder='views/static')

# Carrega as configurações
app.config.from_object('config.Config')

# Registro de rotas 
auth_controller.configure_routes(app)
funcionario_controller.configure_routes(app)
cliente_controller.configure_routes(app)
veiculo_controller.configure_routes(app)
venda_controller.configure_routes(app)

# ========== PÁGINAS PÚBLICAS ==========

# Filtro de formatação monetária BRL 
@app.template_filter('moeda_brl')
def moeda_brl(valor):
    """Formata número no padrão monetário brasileiro, ex: 12345.6 -> R$ 12.345,60"""
    try:
        numero = float(valor) if valor is not None else 0.0
        # Usa separador de milhar com vírgula, depois troca pontuação para padrão BR
        formatado = f"{numero:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') # OLHAR EXEMPLO PROFESSOR
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
        'user_cargo': session.get('user_cargo', ''),
        'user_tipo': session.get('user_tipo', None)
    }

@app.before_request
def proteger_rotas_admin():
    """Verifica se rotas administrativas estão protegidas"""
    rotas_admin = ['/funcionarios', '/clientes', '/vendas']
    if any(request.path.startswith(rota) for rota in rotas_admin):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        # Bloqueia clientes nas rotas administrativas
        if session.get('user_tipo') != 'funcionario':
            return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)