from flask import jsonify, request, current_app as app
from flask_security import verify_password, hash_password
from src.model import Creator, db


datastore = app.security.datastore

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    

    if not email or not password:
        return jsonify({"message" : "invalid inputs"}), 404
    
    user = datastore.find_user(email = email)

    if not user:
        return jsonify({"message" : "invalid email"}), 404
    
    if verify_password(password, user.password):
        return jsonify({'token' : user.get_auth_token(), 'email' : user.email, 'role' : user.roles[0].name, 'id' : user.id, 'creator_id' : user.creator and user.creator.id or None})
    
    return jsonify({'message' : 'password wrong'}), 400

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    username = data.get('username') or None
    artist_name = data.get('artist_name') or None
    
    if not email or not password or role not in ['user', 'creator']:
        return jsonify({"message" : "invalid inputs"}), 404
    
    user = datastore.find_user(email = email)

    if user:
        return jsonify({"message" : "user already exists"}), 404

    try :
        user = datastore.create_user(email = email, password = hash_password(password), roles = [role],username = username, active = True)
        if (role == 'creator'):
            user.creator = Creator(artist_name = artist_name)
        db.session.commit()
        return jsonify({"message" : "user created"}), 200
    except:
        db.session.rollback()
        return jsonify({"message" : "error creating user"}), 400
    