from relationship_graph_app.utils.logging_config import configure_logging
from app import create_app

# Configure logging before creating the app
configure_logging()

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
