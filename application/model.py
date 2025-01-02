from .db import db


class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True)
    nome = db.StringField(required=True)
    sobrenome = db.StringField(required=True)
    dt_nascimento = db.DateTimeField(required=True)
