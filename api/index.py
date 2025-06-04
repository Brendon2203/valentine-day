from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'API funcionando!'

# Necessário para a Vercel
app.debug = True 