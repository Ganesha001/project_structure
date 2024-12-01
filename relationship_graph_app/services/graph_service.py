from gremlin_python.driver import client, serializer
from gremlin_python.driver.protocol import GremlinServerError
from relationship_graph_app.config import Config
from relationship_graph_app.models.vertex import Vertex
import uuid

class GraphService:
    def __init__(self):
        self.client = client.Client(
            Config.COSMOS_ENDPOINT, 
            'g',
            username=f"/dbs/{Config.COSMOS_DATABASE}/colls/{Config.COSMOS_GRAPH}",
            password=Config.COSMOS_KEY,
            message_serializer=serializer.GraphSONMessageSerializer()
        )

    def create_vertex(self, vertex: Vertex):
        """Create a new vertex in the graph"""
        if not vertex.id:
            vertex.id = str(uuid.uuid4())
        
        create_query = f"""
        g.addV('{vertex.label}')
         .property('id', '{vertex.id}')
        """ + ''.join([f".property('{k}', '{v}')" for k, v in vertex.properties.items()])
        
        try:
            result = self.client.submit(create_query)
            return list(result)[0]
        except GremlinServerError as e:
            raise ValueError(f"Error creating vertex: {str(e)}")

    def get_vertex_by_id(self, vertex_id: str):
        """Retrieve a vertex by its ID"""
        query = f"g.V('{vertex_id}')"
        
        try:
            result = self.client.submit(query)
            vertex_data = list(result)[0]
            return Vertex.from_dict(vertex_data)
        except (IndexError, GremlinServerError):
            return None

    def create_edge(self, from_vertex_id: str, to_vertex_id: str, edge_label: str, properties: dict = None):
        """Create an edge between two vertices"""
        properties = properties or {}
        
        create_query = f"""
        g.V('{from_vertex_id}')
         .addE('{edge_label}')
         .to(g.V('{to_vertex_id}'))
        """ + ''.join([f".property('{k}', '{v}')" for k, v in properties.items()])
        
        try:
            result = self.client.submit(create_query)
            return list(result)[0]
        except GremlinServerError as e:
            raise ValueError(f"Error creating edge: {str(e)}")

    def find_connected_vertices(self, vertex_id: str, direction: str = 'both'):
        """Find vertices connected to a given vertex"""
        if direction == 'out':
            query = f"g.V('{vertex_id}').outE().otherV()"
        elif direction == 'in':
            query = f"g.V('{vertex_id}').inE().otherV()"
        else:
            query = f"g.V('{vertex_id}').bothE().otherV()"
        
        try:
            result = self.client.submit(query)
            return [Vertex.from_dict(vertex) for vertex in result]
        except GremlinServerError:
            return []
