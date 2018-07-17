from django.core.exceptions import ObjectDoesNotExist

from core import models


class Usuario:
    def authenticate(self, request, username=None, password=None):
        try:
            user = models.Usuario.objects.get(cns=username)
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = models.Usuario.objects.get(pk=user_id)
            return user
        except ObjectDoesNotExist:
            return None
