import os
from flask import Flask
from relationship_graph_app.routes.relationship_routes import relationship_bp
from relationship_graph_app.config import Config

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Minimal secret key handling
    app.secret_key = Config.get_secret_key()
    
    # Register blueprints
    app.register_blueprint(relationship_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))