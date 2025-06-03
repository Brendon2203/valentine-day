from app import app

# Vercel requer uma função handler
def handler(request, context):
    return app(request) 