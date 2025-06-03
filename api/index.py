from app import app

# Handler para a Vercel
def handler(request):
    return app(request) 