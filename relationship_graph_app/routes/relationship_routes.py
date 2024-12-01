from flask import Blueprint, request, jsonify
from relationship_graph_app.services.graph_service import GraphService
from relationship_graph_app.models.vertex import Vertex

relationship_bp = Blueprint('relationship', __name__)
graph_service = GraphService()

@relationship_bp.route('/vertex', methods=['POST'])
def create_vertex():
    try:
        data = request.json
        vertex = Vertex(
            label=data.get('label', ''),
            properties=data.get('properties', {})
        )
        result = graph_service.create_vertex(vertex)
        return jsonify({'vertex_id': vertex.id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@relationship_bp.route('/vertex/<vertex_id>', methods=['GET'])
def get_vertex(vertex_id):
    vertex = graph_service.get_vertex_by_id(vertex_id)
    if vertex:
        return jsonify(vertex.to_dict()), 200
    return jsonify({'error': 'Vertex not found'}), 404

@relationship_bp.route('/edge', methods=['POST'])
def create_edge():
    try:
        data = request.json
        result = graph_service.create_edge(
            data['from_vertex_id'],
            data['to_vertex_id'],
            data.get('edge_label', 'connected'),
            data.get('properties', {})
        )
        return jsonify({'message': 'Edge created successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@relationship_bp.route('/vertex/<vertex_id>/connections', methods=['GET'])
def get_connections(vertex_id):
    direction = request.args.get('direction', 'both')
    connections = graph_service.find_connected_vertices(vertex_id, direction)
    return jsonify([conn.to_dict() for conn in connections]), 200
