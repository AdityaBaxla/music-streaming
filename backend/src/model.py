from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, unique = True, nullable = False)
    username = db.Column(db.String, unique = True, nullable = True)
    password = db.Column(db.String, nullable = True)
    
    # flask security specific
    fs_uniquifier= db.Column(db.String, unique = True, nullable = False)
    active = db.Column(db.Boolean, default = True)
    confirmed_at = db.Column(db.DateTime(), default = datetime.now())

    roles = db.relationship('Role', backref = 'bearers', secondary = 'user_roles')
    creator = db.relationship('Creator', backref ='user', uselist = False)
    ratings = db.relationship('Rating', backref = 'user')


class Creator(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    artist_name = db.Column(db.String)
    songs = db.relationship('Song', backref = 'creator')
    playlists = db.relationship('Playlist', backref='creator')
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id')) # change the value to user_id


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String, nullable = False)

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Song(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    ratings = db.relationship('Rating', backref='song')  

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    rating = db.Column(db.Integer,nullable=False)
    created_at = db.Column(db.DateTime(), default = datetime.now())

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('creator.id'))
    songs = db.relationship('Song', backref='playlist')
    created_at = db.Column(db.DateTime(), default = datetime.now())