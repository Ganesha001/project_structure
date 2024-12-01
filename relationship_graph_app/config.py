import os
import secrets

class Config:
    # Cosmos DB Gremlin Configuration
    COSMOS_ENDPOINT = os.environ.get('COSMOS_ENDPOINT')
    COSMOS_KEY = os.environ.get('COSMOS_KEY')
    COSMOS_DATABASE = 'RelationshipDB'
    COSMOS_GRAPH = 'RelationshipGraph'
    
    # Optional debug configuration
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'

    # Generate a temporary secret if absolutely needed, but minimize its importance
    @classmethod
    def get_secret_key(cls):
        """
        Generate a temporary secret key if no sensitive operations require it.
        This method prevents the need for a mandatory environment variable.
        """
        return secrets.token_hex(16)