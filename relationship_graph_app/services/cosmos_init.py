import os
import uuid
from gremlin_python.driver import client, serializer

def initialize_cosmos_db(endpoint, key, database='RelationshipDB', graph='RelationshipGraph'):
    """
    Initialize Cosmos DB with some sample vertices and edges
    """
    try:
        gremlin_client = client.Client(
            endpoint, 
            'g',
            username=f"/dbs/{database}/colls/{graph}",
            password=key,
            message_serializer=serializer.GraphSONMessageSerializer()
        )

        # Sample vertices
        vertices = [
            {'id': str(uuid.uuid4()), 'label': 'Person', 'name': 'Alice', 'age': 30},
            {'id': str(uuid.uuid4()), 'label': 'Person', 'name': 'Bob', 'age': 35},
            {'id': str(uuid.uuid4()), 'label': 'Company', 'name': 'TechCorp', 'industry': 'Technology'}
        ]

        # Create vertices
        vertex_ids = []
        for vertex in vertices:
            create_query = f"""
            g.addV('{vertex['label']}')
             .property('id', '{vertex['id']}')
             .property('name', '{vertex['name']}')
            """ + ''.join([f".property('{k}', '{v}')" for k, v in vertex.items() if k not in ['id', 'label', 'name']])
            
            result = gremlin_client.submit(create_query)
            vertex_ids.append(vertex['id'])

        # Create edges
        if len(vertex_ids) >= 3:
            edge_query = f"""
            g.V('{vertex_ids[0]}')
             .addE('works_at')
             .to(g.V('{vertex_ids[2]}'))
             .property('role', 'Employee')
            """
            gremlin_client.submit(edge_query)

        print("Cosmos DB initialized successfully!")
        return True

    except Exception as e:
        print(f"Error initializing Cosmos DB: {e}")
        return False

# Example usage (you would typically call this in a separate script or during deployment)
if __name__ == '__main__':
    endpoint = os.environ.get('COSMOS_ENDPOINT')
    key = os.environ.get('COSMOS_KEY')
    
    if endpoint and key:
        initialize_cosmos_db(endpoint, key)
    else:
        print("Cosmos DB endpoint or key not set in environment variables")
