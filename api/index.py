from flask import Flask
from app import app

# Handler para a Vercel
def handler(request):
    with app.request_context(request):
        return app.handle_request() 