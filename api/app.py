from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
import uuid
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa o app Flask
app = Flask(
    __name__,
    template_folder="../templates",  # Caminho relativo na Vercel
    static_folder="../static"        # Pasta de arquivos estáticos
)

# Configuração do Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME', 'dudvfoo0c'),
    api_key=os.getenv('CLOUDINARY_API_KEY', '338397826413161'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET', 'oXwldGHJHBYj-Ev0H86rSLSJaLc')
)

# Configurações para upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Dicionário para armazenar os pedidos (em memória)
PROPOSALS = {}

# Verifica se o arquivo tem uma extensão permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Página inicial (carrega index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para receber os dados do formulário via POST
@app.route('/create', methods=['POST'])
def create():
    data = request.form
    loved_name = data.get('lovedName', '').strip()
    message = data.get('message', '').strip()
    spotify_link = data.get('spotifyLink', '').strip()

    # Gera um ID único para o pedido
    proposal_id = str(uuid.uuid4())[:8]
    
    # Upload de arquivos para o Cloudinary
    files = request.files.getlist('photos[]')
    uploaded_urls = []

    for file in files:
        if file and allowed_file(file.filename):
            try:
                # Upload para o Cloudinary com pasta específica
                result = cloudinary.uploader.upload(
                    file,
                    folder="Dynamic folders",  # Especifica a pasta no Cloudinary
                    resource_type="auto"
                )
                uploaded_urls.append(result['secure_url'])
            except Exception as e:
                print(f"Erro ao fazer upload: {str(e)}")
                continue

    # Armazena os dados do pedido
    proposal_data = {
        'id': proposal_id,
        'loved_name': loved_name,
        'message': message,
        'spotify_link': spotify_link,
        'photos': uploaded_urls
    }
    
    PROPOSALS[proposal_id] = proposal_data

    # Retorna os dados com o ID único
    return jsonify({
        'id': proposal_id,
        'url': f'/proposal/{proposal_id}',
        'lovedName': loved_name,
        'message': message,
        'spotifyLink': spotify_link,
        'photos': uploaded_urls
    })

@app.route('/proposal/<proposal_id>')
def view_proposal(proposal_id):
    proposal = PROPOSALS.get(proposal_id)
    if not proposal:
        return "Pedido não encontrado", 404
    return render_template('proposal.html', proposal=proposal)

# Necessário para a Vercel rodar corretamente
app = app
