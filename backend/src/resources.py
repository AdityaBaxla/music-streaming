from flask import abort, jsonify, request
from flask_restful import Resource, Api, fields, marshal_with
from sqlalchemy import or_
from flask_security import current_user, auth_required
from sqlalchemy.orm import joinedload

from src.model import Creator, Playlist, Rating, Role, Song, User, db

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
creator_fields = {
    'creator_id': fields.Integer,
    'artist_name': fields.String,
    'user_id' : fields.Integer,
}

song_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description' : fields.String,
    'creator_id': fields.Integer,
    'playlist_id': fields.Integer,
    'creator': fields.Nested(creator_fields),  # Nested Creator
    'ratings': fields.List(fields.Nested({
        'id': fields.Integer,
        'user_id': fields.Integer,
        'song_id': fields.Integer,
        'rating': fields.Integer,
        'created_at': fields.DateTime
    }))
}


playlist_fields = {
    'id' : fields.Integer,
    'creator_id': fields.Integer,
    'name' : fields.String,
    'songs': fields.List(fields.Nested(song_fields)),
    'created_at': fields.DateTime
}

creator_fields = {
    'creator_id' : fields.Integer,
    'artist_name' : fields.String,
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

    # def put(self, creator_id):
    #     creator = get_instance_or_abort(Creator, creator_id)
    #     data = request.get_json()
    #     creator.creator_id = data.get('creator_id', creator.creator_id)
    #     db.session.commit()
    #     return {"message": "Creator updated successfully"}

    # def delete(self, creator_id):
    #     creator = get_instance_or_abort(Creator, creator_id)
    #     db.session.delete(creator)
    #     db.session.commit()
    #     return {"message": "Creator deleted successfully"}

# Song Resource
class SongResource(Resource):
    @marshal_with(song_fields)
    def get(self, song_id = None):
        if song_id:
            song = Song.query.get(song_id)
            return song
        songs = Song.query.all()
        return songs


    # @marshal_with(song_fields)
    # def get(self, song_id=None):
    #     if song_id:
    #         # Fetch a single song by ID or return 404
    #         song = get_instance_or_abort(Song, song_id)
    #         print(song.creator)
    #         return self.serialize_song(song)
        
    #     # Fetch all songs with their creators
    #     songs = Song.query.options(joinedload(Song.creator)).all()
        
    #     # Serialize each song
    #     serialized_songs = [self.serialize_song(song) for song in songs]
        
    #     return jsonify(serialized_songs)

    # def serialize_song(self, song):
    #     """Convert a Song object into a dictionary, including nested creator data."""
    #     return {
    #         "id": song.id,
    #         "name": song.name,
    #         "description": song.description,
    #         "creator_id": song.creator_id,
    #         "playlist_id": song.playlist_id,
    #         "creator": {
    #             "id": song.creator.id if song.creator else None,
    #             "artist_name": song.creator.artist_name if song.creator else None,
    #         },
    #         "ratings": [
    #             {
    #                 "id": rating.id,
    #                 "user_id": rating.user_id,
    #                 "song_id": rating.song_id,
    #                 "rating": rating.rating,
    #                 "created_at": rating.created_at.isoformat(),
    #             }
    #             for rating in song.ratings
    #         ],
    #     }

    @auth_required()
    def post(self):
        data = request.get_json()
        print(data)
        if (current_user.roles[0] != 'creator'):
            return {'message' : 'role not authorized'}
        creator_id = current_user.creator.creator_id 
        new_song = Song( name = data.get('name'), description = data.get('description'),playlist_id=data.get('playlist_id'), creator_id = creator_id)
        db.session.add(new_song)
        db.session.commit()
        return {"message": "Song created successfully", "id": new_song.id}, 201

    @auth_required()
    def put(self, song_id):
        song = Song.query.get_or_404(song_id)
        # check if the the song is created by the user
        print(current_user.creator.songs)
        if (current_user.roles[0] != 'creator'):
            return {'message' : 'role not authorized'}
        creator_id = current_user.creator.creator_id 

        data = request.get_json()
        song.creator_id = data.get('creator_id', song.creator_id) # transfer ownership
        song.playlist_id = data.get('playlist_id', song.playlist_id)  # add song to playlist
        db.session.commit()
        return {"message": "Song updated successfully"}

    def delete(self, song_id):
        song = get_instance_or_abort(Song, song_id)
        creator_id = current_user.creator.creator_id
        if song.creator.creator_id != creator_id:
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

    @auth_required()
    def post(self):
        print('before')
        data = request.get_json()
        print(data)
        new_playlist = Playlist(creator_id=current_user.creator.creator_id, name = data.get('name'))
        db.session.add(new_playlist)
        db.session.commit()
        return {"message": "Playlist created successfully", "id": new_playlist.id}, 201
    
    @auth_required()
    def put(self, playlist_id):
        playlist = get_instance_or_abort(Playlist, playlist_id)
        creator_id = current_user.creator.creator_id
        if playlist.creator_id != creator_id:
            return jsonify({'message' : 'your are not the creator' })
        
        data = request.get_json()
        playlist.creator_id = data.get('user_id', playlist.creator_id)
        db.session.commit()
        return {"message": "Playlist updated successfully"}

    @auth_required()
    def delete(self, playlist_id):
        playlist = get_instance_or_abort(Playlist, playlist_id)
        creator_id = current_user.creator.creator_id
        if playlist.creator_id != creator_id:
            return jsonify({'message' : 'your are not the creator' })
        
        db.session.delete(playlist)
        db.session.commit()

class RatingResource(Resource):

    @auth_required()
    def post(self, song_id):
        song = Song.query.get_or_404(song_id)
        data = request.get_json()

        rating = Rating(song_id = song_id, user_id = current_user.id, rating = data.get('rating'))
        db.session.add(rating)
        db.session.commit()
        return jsonify({'message' : 'rating created'})

# Add resources to the API
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(CreatorResource, '/creators', '/creators/<int:creator_id>')
api.add_resource(SongResource, '/songs', '/songs/<int:song_id>')
api.add_resource(PlaylistResource, '/playlists', '/playlists/<int:playlist_id>')
api.add_resource(RatingResource, '/songs/<int:song_id>/ratings', )


        
