from flask import jsonify, request, current_app as app, send_file
from flask_security import verify_password, hash_password
from src.model import Creator, Song, db


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
        return jsonify({'token' : user.get_auth_token(), 'email' : user.email, 'role' : user.roles[0].name, 'id' : user.id, 'creator_id' : user.creator and user.creator.creator_id or None})
    
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
    
# testing if data has been correctly sedn
# from io import BytesIO
# from flask import send_file

# @app.get('/download/<int:song_id>')
# def download(song_id):
#     song = Song.query.get(song_id)
#     if not song or not song.image_file:
#         return jsonify({"message": "Image not found"}), 404

#     # Convert binary data to a file-like object
#     image_file = BytesIO(song.image_file)

#     # Send the file with the correct download name
#     return send_file(image_file, as_attachment=True, download_name='image.png', mimetype=song.image_mimetype)


from io import BytesIO

@app.get('/download/<int:song_id>')
def download(song_id):
    song = Song.query.get(song_id)
    if not song or not song.image_file:
        return jsonify({"message": "Image not found"}), 404

    # Map MIME types to extensions
    extension_map = {
        'image/png': 'png',
        'image/jpeg': 'jpg',
        'image/jpg': 'jpg',
        'image/svg+xml': 'svg',
    }
    file_extension = extension_map.get(song.image_mimetype, 'bin')  # Default to .bin if unknown type

    # Convert binary data to file-like object
    image_file = BytesIO(song.image_file)

    # Send file with correct extension
    return send_file(
        image_file,
        as_attachment=True,
        download_name=f'image.{file_extension}',
        mimetype=song.image_mimetype
    )