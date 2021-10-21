from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    # favoritespeople_id = db.Column(db.Integer, db.ForeignKey('favoritespeople.id'))
    # favoritespeople = db.relationship('FavoritesPeople', backref='user')

    def __repr__(self):
        return '<User %r>' % self.email

    # def __init__(self, email, password):
    #     self.email = email
    #     self.password = password
    #     self.is_active = True

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }
    
    # @classmethod
    # def registrar(cls, email, password):
    #     new_user = cls(
    #         email.lower(),
    #         password
           
    #     )
    #     return new_user

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), unique=True)
    picture_url = db.Column(db.String(250))

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture_url": self.picture_url
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), unique=True)
    picture_url = db.Column(db.String(250))

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture_url": self.picture_url
        }


class FavoritesPeople(db.Model):
    __tablename__ = 'favoritespeople'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), primary_key=True)
    user = db.relationship(User)
    people = db.relationship(People)

    def __repr__(self):
        return '<FavoritesPeople %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id
        }