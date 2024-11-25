from flask import abort, jsonify, request
from flask_restful import Resource, Api, fields, marshal_with
from sqlalchemy import or_
from flask_security import current_user, auth_required

from src.model import Creator, Playlist, Role, Song, User, db

api = Api(prefix='/api')


# Helper function for validation
def get_instance_or_404(model, instance_id):
    instance = model.query.get(instance_id)
    if not instance:
        return {"message": f"{model.__name__} with id {instance_id} not found"}, 404
    return instance

user_list_fields = {
    'id' : fields.Integer,
    'email' : fields.String,
    'username' : fields.String,
}

class UserResource(Resource):
    
    @marshal_with(user_list_fields)
    def get(self, user_id = None):

        # if we get user_id then return the user id 
        if user_id:
            return User.query.get(user_id)
        
        query = request.args.get('query')

        if query:
            users = User.query.join(User.roles).filter(
                or_(Role.name == 'user',Role.name == 'creator'),
                User.active == True,
                User.email.ilike(f'%{query}%')
            ).all()
        else : 
            users = User.query.join(User.roles).filter(or_(Role.name == 'user',Role.name == 'creator')).all()

        return users
    # def put(self, user_id):
    #     user = get_instance_or_404(User, user_id)
    #     if isinstance(user, dict):  # Error handling
    #         return user
    #     data = request.get_json()
    #     user.email = data.get('email', user.email)
    #     user.username = data.get('username', user.username)
    #     db.session.commit()
    #     return jsonify({"message": "User updated successfully"})

    # def delete(self, user_id):
    #     user = get_instance_or_404(User, user_id)
    #     if isinstance(user, dict):  # Error handling
    #         return user
    #     db.session.delete(user)
    #     db.session.commit()
    #     return jsonify({"message": "User deleted successfully"})

song_fields = {
    'id': fields.Integer,
    'creator_id': fields.Integer,
    'playlist_id': fields.Integer,
    'ratings': fields.List(fields.Nested({
        'id': fields.Integer,
        'user_id': fields.Integer,
        'song_id': fields.Integer,
        'rating': fields.Integer,
        'created_at': fields.DateTime
    }))
}

playlist_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,  # Creator ID in this context
    'songs': fields.List(fields.Nested(song_fields)),
    'created_at': fields.DateTime
}
creator_fields = {
    'id' : fields.Integer,
    'user' : fields.Nested(user_list_fields),
    'songs' : fields.List(fields.Nested(song_fields)),
    'playlists' : fields.List(fields.Nested(playlist_fields)), 
}


def get_instance_or_abort(model, id):
    instance = model.query.get(id)
    if not instance:
        abort(404, description=f"{model.__name__} with ID {id} not found.")
    return instance

# Creator Resource
class CreatorResource(Resource):
    @marshal_with(creator_fields)
    def get(self, creator_id=None):
        if creator_id:
            return get_instance_or_abort(Creator, creator_id)
        creators = Creator.query.all()
        return creators

    def post(self):
        data = request.get_json()
        new_creator = Creator(creator_id=data['creator_id'])
        db.session.add(new_creator)
        db.session.commit()
        return {"message": "Creator created successfully", "id": new_creator.id}, 201

    def put(self, creator_id):
        creator = get_instance_or_abort(Creator, creator_id)
        data = request.get_json()
        creator.creator_id = data.get('creator_id', creator.creator_id)
        db.session.commit()
        return {"message": "Creator updated successfully"}

    def delete(self, creator_id):
        creator = get_instance_or_abort(Creator, creator_id)
        db.session.delete(creator)
        db.session.commit()
        return {"message": "Creator deleted successfully"}

# Song Resource
class SongResource(Resource):
    @marshal_with(song_fields)
    def get(self, song_id=None):
        if song_id:
            return get_instance_or_abort(Song, song_id)
        songs = Song.query.all()
        return songs

    @auth_required()
    def post(self):
        data = request.get_json()
        user_id = current_user.id 
        new_song = Song( name = data.get('name'), description = data.get('description'),playlist_id=data.get('playlist_id'), creator_id = user_id)
        db.session.add(new_song)
        db.session.commit()
        return {"message": "Song created successfully", "id": new_song.id}, 201

    @auth_required()
    def put(self, song_id):
        song = get_instance_or_abort(Song, song_id)
        # check if the the song is created by the user
        print(current_user.creator.id)
        creator_id = current_user.id
        if song.creator_id != creator_id:
            return jsonify({'message' : 'your are not the creator' })
        
        data = request.get_json()
        song.creator_id = data.get('creator_id', song.creator_id) # transfer ownership
        song.playlist_id = data.get('playlist_id', song.playlist_id)  # add song to playlist
        db.session.commit()
        return {"message": "Song updated successfully"}

    def delete(self, song_id):
        song = get_instance_or_abort(Song, song_id)
        creator_id = current_user.id
        if song.creator_id != creator_id:
            return jsonify({'message' : 'your are not the creator' })
        

        db.session.delete(song)
        db.session.commit()
        return {"message": "Song deleted successfully"}

# Playlist Resource
class PlaylistResource(Resource):
    @marshal_with(playlist_fields)
    def get(self, playlist_id=None):
        if playlist_id:
            return get_instance_or_abort(Playlist, playlist_id)
        playlists = Playlist.query.all()
        return playlists

    @auth_required
    def post(self):
        
        data = request.get_json()
        new_playlist = Playlist(user_id=data['user_id'])
        db.session.add(new_playlist)
        db.session.commit()
        return {"message": "Playlist created successfully", "id": new_playlist.id}, 201
    
    @auth_required()
    def put(self, playlist_id):
        playlist = get_instance_or_abort(Playlist, playlist_id)
        creator_id = current_user.id
        if playlist.creator_id != creator_id:
            return jsonify({'message' : 'your are not the creator' })
        
        data = request.get_json()
        playlist.user_id = data.get('user_id', playlist.user_id)
        db.session.commit()
        return {"message": "Playlist updated successfully"}

    @auth_required
    def delete(self, playlist_id):
        playlist = get_instance_or_abort(Playlist, playlist_id)
        creator_id = current_user.id
        if playlist.creator_id != creator_id:
            return jsonify({'message' : 'your are not the creator' })
        
        db.session.delete(playlist)
        db.session.commit()
  

# Add resources to the API
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(CreatorResource, '/creators', '/creators/<int:creator_id>')
api.add_resource(SongResource, '/songs', '/songs/<int:song_id>')
api.add_resource(PlaylistResource, '/playlists', '/playlists/<int:playlist_id>')

