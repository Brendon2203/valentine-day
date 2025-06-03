from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename

# Inicializa o app Flask
app = Flask(
    __name__,
    template_folder="../templates",  # Caminho relativo na Vercel
    static_folder="../static"        # Pasta de arquivos estáticos
)

# Configurações para upload
UPLOAD_FOLDER = '../static/uploads'  # Caminho relativo ajustado para Vercel
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Garante que a pasta de uploads exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

    # Upload de arquivos
    files = request.files.getlist('photos[]')

    saved_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            saved_files.append(url_for('uploaded_file', filename=filename))

    # Retorna os dados para renderização no frontend
    return jsonify({
        'lovedName': loved_name,
        'message': message,
        'spotifyLink': spotify_link,
        'photos': saved_files
    })

# Rota para servir imagens carregadas
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Necessário para a Vercel rodar corretamente
app = app
