#!/bin/bash
# Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

# Make startup script executable
chmod +x startup.sh

# Optional: Initialize database (uncomment if needed)
# python -c "from relationship_graph_app.services.cosmos_init import initialize_cosmos_db; initialize_cosmos_db(os.environ['COSMOS_ENDPOINT'], os.environ['COSMOS_KEY'])"

# Start Gunicorn
gunicorn --config gunicorn.conf.py run:app
