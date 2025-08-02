import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.payment import payment_bp
from src.routes.video import video_bp
from src.routes.social import social_bp
from src.routes.whatsapp import whatsapp_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB para upload de vídeos

# CORS - permitir requisições de qualquer origem
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"])

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(payment_bp, url_prefix='/api')
app.register_blueprint(video_bp, url_prefix='/api')
app.register_blueprint(social_bp, url_prefix='/api')
app.register_blueprint(whatsapp_bp, url_prefix='/api')

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Criar tabelas
with app.app_context():
    db.create_all()

# Configurar pasta do frontend
FRONTEND_DIR = '/home/ubuntu/video-ai-html-frontend'

# Rota para servir arquivos estáticos e SPA
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Se for uma rota da API, não processar aqui
    if path.startswith('api/'):
        return "API endpoint not found", 404
    
    # Se for um arquivo específico (tem extensão)
    if path and '.' in path:
        file_path = os.path.join(FRONTEND_DIR, path)
        if os.path.exists(file_path):
            return send_from_directory(FRONTEND_DIR, path)
    
    # Para rotas específicas do frontend
    if path in ['login', 'register', 'dashboard', 'subscription', 'payment', 'videos', 'social', 'whatsapp', 'profile']:
        html_file = f"{path}.html"
        file_path = os.path.join(FRONTEND_DIR, html_file)
        if os.path.exists(file_path):
            return send_from_directory(FRONTEND_DIR, html_file)
    
    # Página inicial ou fallback
    index_path = os.path.join(FRONTEND_DIR, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(FRONTEND_DIR, 'index.html')
    else:
        return "Frontend not found", 404

# Rota de status da API
@app.route('/api/status')
def api_status():
    return {
        'status': 'online',
        'version': '1.0.0',
        'features': [
            'user_authentication',
            'subscription_management',
            'payment_processing',
            'video_upload_processing',
            'ai_video_analysis',
            'social_media_integration',
            'whatsapp_billing'
        ]
    }

# Rota de informações da API
@app.route('/api/info')
def api_info():
    return {
        'name': 'Plataforma Video AI',
        'description': 'Plataforma completa para análise de vídeos com IA e publicação em redes sociais',
        'version': '1.0.0',
        'endpoints': {
            'authentication': [
                'POST /api/register',
                'POST /api/login',
                'GET /api/profile',
                'PUT /api/profile'
            ],
            'subscriptions': [
                'GET /api/subscriptions/plans',
                'POST /api/subscriptions',
                'GET /api/subscriptions',
                'POST /api/subscriptions/{id}/cancel'
            ],
            'payments': [
                'POST /api/payments/create',
                'POST /api/payments/{id}/confirm',
                'GET /api/payments/{id}/qr-code',
                'POST /api/payments/{id}/process-card'
            ],
            'videos': [
                'POST /api/videos/upload',
                'POST /api/videos/{id}/process',
                'GET /api/videos',
                'GET /api/videos/{id}',
                'POST /api/videos/{id}/generate-clips'
            ],
            'social_media': [
                'GET /api/social/platforms',
                'POST /api/social/connect/{platform}',
                'POST /api/social/post',
                'GET /api/social/posts'
            ],
            'whatsapp': [
                'GET /api/whatsapp/config',
                'PUT /api/whatsapp/config',
                'POST /api/whatsapp/verify-phone',
                'POST /api/whatsapp/test-message'
            ]
        }
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
