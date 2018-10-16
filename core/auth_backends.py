"""
Autenticação personalizada.
"""
from core import models


class Auth():
    """Base."""

    def authenticate(self, username=None, password=None, **kwargs):
        """Autentica."""

        try:

            user = self.UserModel.objects.get(cns=username)

            if user.check_password(password):

                return user

        except self.UserModel.DoesNotExist:

            self.UserModel().set_password(password)

    def get_user(self, user_id):
        """Retorna o usuário."""

        try:

            return self.UserModel.objects.get(pk=user_id)

        except self.UserModel.DoesNotExist:

            return None


class Odontologo(Auth):
    "Autentica Odontólogo."

    def __init__(self):

        self.UserModel = models.Odontologo


class ACS(Auth):
    "Autentica ACS."

    def __init__(self):

        self.UserModel = models.ACS


class Usuario(Auth):
    "Autentica Usuários."

    def __init__(self):

        self.UserModel = models.Usuario
