from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader

# Inicializa o app Flask
app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Configuração do Cloudinary
cloudinary.config(
    cloud_name='dudvfoo0c',
    api_key='338397826413161',
    api_secret='oXwldGHJHBYj-Ev0H86rSLSJaLc'
)

# Configurações para upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Dicionário para armazenar os pedidos (em memória)
PROPOSALS = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    data = request.form
    loved_name = data.get('lovedName', '').strip()
    message = data.get('message', '').strip()
    spotify_link = data.get('spotifyLink', '').strip()

    # Gera um ID único simples baseado no timestamp
    from datetime import datetime
    proposal_id = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Upload de arquivos para o Cloudinary
    files = request.files.getlist('photos[]')
    uploaded_urls = []

    for file in files:
        if file and allowed_file(file.filename):
            try:
                result = cloudinary.uploader.upload(file)
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

# Necessário para a Vercel
app = app
