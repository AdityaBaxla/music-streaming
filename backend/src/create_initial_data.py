from flask import current_app as app
from src.model import Creator, db
from flask_security import SQLAlchemyUserDatastore, hash_password

with app.app_context():
    db.create_all()

    userdatastore : SQLAlchemyUserDatastore = app.security.datastore

    userdatastore.find_or_create_role(name = 'admin', description = 'superuser')
    userdatastore.find_or_create_role(name = 'user', description = 'general user')
    userdatastore.find_or_create_role(name = 'creator', description = 'music creator')

    if (not userdatastore.find_user(email = 'admin@study.iitm.ac.in')):
        userdatastore.create_user(email = 'admin@study.iitm.ac.in',username = "admin", password = hash_password('pass'), roles = ['admin'] )
    if (not userdatastore.find_user(email = 'user01@study.iitm.ac.in')):
        userdatastore.create_user(email = 'user01@study.iitm.ac.in', username = "user01",password = hash_password('pass'), roles = ['user'] ) # for testing
    if (not userdatastore.find_user(email = 'creator01@study.iitm.ac.in')):
        user = userdatastore.create_user(email = 'creator01@study.iitm.ac.in',username = "creator01", password = hash_password('pass'), roles = ['creator'] ) # for testing
        user.creator = Creator(artist_name = "Mars")
        

    db.session.commit()