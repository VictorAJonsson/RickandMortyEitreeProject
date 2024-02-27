from flask import Flask, jsonify, request
from models.models import db, Character
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/rickandmorty'

# Inicializar a extensão SQLAlchemy
db.init_app(app)

# Abre o CORS da aplicacao
CORS(app)

# Rota para obter detalhes de um personagem pelo ID
@app.route('/api/characters/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    try:
        # Busca o personagem pelo ID
        character = Character.query.get(character_id)

        # Verifica se o personagem foi encontrado
        if character:
            # Construir um dicionário com informações do personagem
            character_details = {
                'id': character.id,
                'name': character.name,
                'status': character.status,
                'species': character.species,
                'type': character.type,
                'gender': character.gender,
                'origin_name': character.origin_name,
                'location_name': character.location_name,
                'image_url': character.image_url
            }
            return jsonify({
            "success": True,
            "message": "Character Found! c: ",
            "data": character_details
            })
            
        else:
            return jsonify({
                "success": False,
                "message": 'Character not found! :c ',
                "data": None
                }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "There was an error :c ",
            "data": None
            }), 500

# Rota para obter todos os personagens
@app.route('/api/characters', methods=['GET'])
def get_characters():
    try:
        partial_name = request.args.get('partial_name', '')
        page = int(request.args.get('page', 0))
        per_page = 20

        # Obtém personagens paginados e ordenados por similaridade
        characters = Character.query.filter(Character.name.ilike(f'%{partial_name}%')).paginate(page=page, per_page=per_page, error_out=False)

        # Construir uma lista de dicionários para representar os personagens
        character_list = [{
            'id': character.id,
            'name': character.name,
            'species': character.species,
            'image_url': character.image_url
        } for character in characters]

        # Calcular o número total de páginas
        total_pages = characters.pages

        return jsonify({
            "success": True,
            "message": "Characters Found! c: ",
            "data": {
                'character_list': character_list, 
                'total_pages': total_pages
                }
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "There was an error :c ",
            "data": None
            }), 500

if __name__ == '__main__':
    app.run(debug=True)
