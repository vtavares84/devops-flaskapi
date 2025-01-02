from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_mongoengine import MongoEngine
from mongoengine import NotUniqueError

app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'host': 'mongodb',
    'port': 27017,
    'username': 'admin',
    'password': 'admin'
}
db = MongoEngine(app)



_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'nome',
    type=str,
    required=True,
    help="This field cannot be blank."
)
_user_parser.add_argument(
    'sobrenome',
    type=str,
    required=True,
    help="This field cannot be blank."
)
_user_parser.add_argument(
    'cpf',
    type=str,
    required=True,
    help="This field cannot be blank."
)
_user_parser.add_argument(
    'email',
    type=str,
    required=True,
    help="This field cannot be blank."
)
_user_parser.add_argument(
    'dt_nascimento',
    type=str,
    required=True,
    help="This field cannot be blank."
)

class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True)
    nome = db.StringField(required=True)
    sobrenome = db.StringField(required=True)
    dt_nascimento = db.DateTimeField(required=True)


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())


class User(Resource):
    def post(self):
        data = _user_parser.parse_args()

        try:
            response = UserModel(**data).save()
            return {"message": "Usuário %s foi criado com sucesso!" % response.id}
        except NotUniqueError:
            return {"message": "CPF já foi utilizado na base de dados"}, 400
                

    def get(self, cpf):
        response = UserModel.objects(cpf=cpf)
        if response:
            return jsonify(response)
        
        return {"message": "Usuário não foi encontrado no banco de dados"}, 400


api.add_resource(Users, '/users')
api.add_resource(User, '/user', '/user/<string:cpf>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
