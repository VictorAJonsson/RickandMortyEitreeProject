# app.py
from flask import Flask, jsonify, request
from models.models import db, Character
from flask_cors import CORS
from dotenv import load_dotenv 
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

# Initialize the SQLAlchemy
db.init_app(app)

# Open the CORS
CORS(app)

# Route to obtain details of a character by ID
@app.route('/api/characters/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    try:
        # Search the character by ID
        character = Character.query.get(character_id)

        # Checks if the character was found
        if character:
            # Build a Json with character information
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

# Route to get all characters by partial name
@app.route('/api/characters', methods=['GET'])
def get_characters():
    try:
        partial_name = request.args.get('partial_name', '')
        page = int(request.args.get('page', 0))
        per_page = 20

        # Gets paginated characters ordered by similarity
        characters = Character.query.filter(Character.name.ilike(f'%{partial_name}%')).paginate(page=page, per_page=per_page, error_out=False)

        # Build a Json to store character data
        character_list = [{
            'id': character.id,
            'name': character.name,
            'status': character.status,
            'species': character.species,
            'image_url': character.image_url
        } for character in characters]

        # Calculate the total number of pages
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
