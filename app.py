import os
import sys
import traceback
from flask import Flask, jsonify

def create_app():
    try:
        from relationship_graph_app.routes.relationship_routes import relationship_bp
        from relationship_graph_app.config import Config

        app = Flask(__name__)
        
        # Load configuration
        app.config.from_object(Config)
        
        # Register blueprints
        app.register_blueprint(relationship_bp, url_prefix='/api')
        
        # Error handler for unhandled exceptions
        @app.errorhandler(Exception)
        def handle_exception(e):
            # Log the error
            app.logger.error(f"Unhandled Exception: {str(e)}")
            traceback.print_exc()
            
            # Return a generic error response
            return jsonify({
                'error': 'Internal Server Error', 
                'message': str(e)
            }), 500
        
        return app
    
    except Exception as e:
        print(f"Error creating app: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise

# Explicit app creation for Gunicorn
app = create_app()
