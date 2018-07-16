from django.contrib.auth.hashers import check_password

from core import models


class Usuario:

    def authenticate(self, request, username=None, password=None):

        try:

            user = models.Usuario.objects.get(cns=username)

        except user.DoesNotExist:

            return None

        return user

    def get_user(self, user_id):

        try:

            user = models.Usuario.objects.get(pk=user_id)

        except user.DoesNotExist:

            return None

        return user
