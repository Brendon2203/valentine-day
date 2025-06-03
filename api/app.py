from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
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

    # Retorna os dados para renderização no frontend
    return jsonify({
        'lovedName': loved_name,
        'message': message,
        'spotifyLink': spotify_link,
        'photos': uploaded_urls
    })

# Necessário para a Vercel rodar corretamente
app = app
