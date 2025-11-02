from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from models import veiculo_model
import os
from werkzeug.utils import secure_filename

veiculo_bp = Blueprint('veiculo', __name__)

# Configuração de upload
UPLOAD_FOLDER = 'views/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Você precisa fazer login para acessar esta página", "error")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def criar_pasta_uploads():
    """Cria pasta de uploads se não existir"""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

def deletar_foto(foto_path):
    """Deleta uma foto do sistema de arquivos se ela existir"""
    if foto_path and os.path.exists(foto_path):
        try:
            os.remove(foto_path)
        except Exception as e:
            print(f"Erro ao deletar foto: {str(e)}")  # Log do erro, mas não interrompe o fluxo

@veiculo_bp.route('/veiculos')
def listar_veiculos():
    """Lista todos os veículos (página pública quando não logado)"""
    try:
        veiculos = veiculo_model.listar_veiculos()
    except Exception as e:
        flash("Não foi possível carregar os veículos. Verifique a conexão com o banco de dados.", "error")
        veiculos = []
    return render_template('veiculos.html', veiculos=veiculos, logged_in='user_id' in session)

@veiculo_bp.route('/veiculos_disponiveis')
def listar_veiculos_disponiveis():
    """Lista veículos disponíveis (página pública)"""
    try:
        veiculos = veiculo_model.listar_veiculos_disponiveis()
    except Exception as e:
        flash("Não foi possível carregar os veículos disponíveis. Verifique a conexão com o banco de dados.", "error")
        veiculos = []
    return render_template('veiculos_disponiveis.html', veiculos=veiculos)

@veiculo_bp.route('/veiculo/novo')
@login_required
def formulario_novo_veiculo():
    """Exibe formulário para novo veículo"""
    return render_template('form_veiculo.html', veiculo=None)

@veiculo_bp.route('/veiculo/novo', methods=['POST'])
@login_required
def novo_veiculo():
    """Cria um novo veículo com upload de foto"""
    try:
        marca = request.form['marca'].strip()
        modelo = request.form['modelo'].strip()
        ano = request.form['ano']
        preco = request.form['preco']
        cor = request.form.get('cor', '').strip()
        combustivel = request.form.get('combustivel', '').strip()
        km_rodados = request.form.get('km_rodados', '0')
        
        # Validações
        if not marca or not modelo or not ano or not preco:
            flash("Todos os campos são obrigatórios!", "error")
            return redirect(url_for('veiculo.formulario_novo_veiculo'))
        
        foto = None
        
        # Processa upload de foto
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename != '' and allowed_file(file.filename):
                # Cria pasta se não existir
                criar_pasta_uploads()
                
                # Gera nome seguro para o arquivo
                filename = secure_filename(file.filename)
                # Adiciona timestamp para evitar conflitos
                import time
                filename = f"{int(time.time())}_{filename}"
                
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                # Normaliza o caminho para usar barras (/)
                foto = filepath.replace('\\', '/')
        
        # Adiciona veículo
        veiculo_model.adicionar_veiculo(marca, modelo, ano, preco, foto, km_rodados, cor, combustivel)
        flash("Veículo cadastrado com sucesso!", "success")
        return redirect(url_for('veiculo.listar_veiculos'))
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for('veiculo.formulario_novo_veiculo'))
    except Exception as e:
        flash(f"Erro ao cadastrar veículo: {str(e)}", "error")
        return redirect(url_for('veiculo.formulario_novo_veiculo'))

@veiculo_bp.route('/veiculo/editar/<int:id>')
@login_required
def formulario_editar_veiculo(id):
    """Exibe formulário para editar veículo"""
    veiculo = veiculo_model.obter_veiculo(id)
    if not veiculo:
        flash("Veículo não encontrado!", "error")
        return redirect(url_for('veiculo.listar_veiculos'))
    
    return render_template('form_veiculo.html', veiculo=veiculo)

@veiculo_bp.route('/veiculo/editar/<int:id>', methods=['POST'])
@login_required
def editar_veiculo(id):
    """Atualiza um veículo"""
    try:
        marca = request.form['marca'].strip()
        modelo = request.form['modelo'].strip()
        ano = request.form['ano']
        preco = request.form['preco']
        disponivel = request.form.get('disponivel') == 'on'
        cor = request.form.get('cor', '').strip()
        combustivel = request.form.get('combustivel', '').strip()
        km_rodados = request.form.get('km_rodados', '0')
        
        # Validações
        if not marca or not modelo or not ano or not preco:
            flash("Todos os campos são obrigatórios!", "error")
            return redirect(url_for('veiculo.formulario_editar_veiculo', id=id))
        
        # Busca a foto atual do veículo
        veiculo_atual = veiculo_model.obter_veiculo(id)
        foto_antiga = veiculo_atual.get('foto') if veiculo_atual else None
        
        # Processa upload de nova foto (se fornecida)
        foto = None
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename != '' and allowed_file(file.filename):
                criar_pasta_uploads()
                
                filename = secure_filename(file.filename)
                import time
                filename = f"{int(time.time())}_{filename}"
                
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                # Normaliza o caminho para usar barras (/)
                foto = filepath.replace('\\', '/')
                
                # Deleta a foto antiga se existir e se for diferente da nova
                if foto_antiga and foto_antiga != foto:
                    deletar_foto(foto_antiga)
        
        # Atualiza veículo
        veiculo_model.atualizar_veiculo(id, marca, modelo, ano, preco, disponivel, km_rodados, cor, combustivel, foto)
        flash("Veículo atualizado com sucesso!", "success")
        return redirect(url_for('veiculo.listar_veiculos'))
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for('veiculo.formulario_editar_veiculo', id=id))
    except Exception as e:
        flash(f"Erro ao atualizar veículo: {str(e)}", "error")
        return redirect(url_for('veiculo.formulario_editar_veiculo', id=id))

@veiculo_bp.route('/veiculo/excluir/<int:id>')
@login_required
def excluir_veiculo(id):
    """Exclui um veículo"""
    try:
        # Verifica se veículo tem vendas
        if veiculo_model.veiculo_tem_vendas(id):
            flash("Não é possível excluir veículo que já possui vendas associadas!", "error")
            return redirect(url_for('veiculo.listar_veiculos'))
        
        # Busca o veículo para pegar a foto
        veiculo = veiculo_model.obter_veiculo(id)
        
        # Exclui veículo
        veiculo_model.excluir_veiculo(id)
        
        # Deleta a foto do veículo se existir
        if veiculo and veiculo.get('foto'):
            deletar_foto(veiculo['foto'])
        
        flash("Veículo excluído com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao excluir veículo: {str(e)}", "error")
    
    return redirect(url_for('veiculo.listar_veiculos'))