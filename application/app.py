from flask import jsonify
from flask_restful import Resource, reqparse
from .model import UserModel
from mongoengine import NotUniqueError


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


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())


class User(Resource):
    def post(self):
        data = _user_parser.parse_args()

        try:
            response = UserModel(**data).save()
            return {"message":
                    "Usuário %s foi criado com sucesso!" % response.id}
        except NotUniqueError:
            return {"message": "CPF já foi utilizado na base de dados"}, 400

    def get(self, cpf):
        response = UserModel.objects(cpf=cpf)
        if response:
            return jsonify(response)

        return {"message": "Usuário não foi encontrado no banco de dados"}, 400
