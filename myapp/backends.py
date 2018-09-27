from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
User = get_user_model()

class authBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        #if user.is_active and user.password == password:
        if user.is_active and user.check_password(raw_password=password):
            return user

        return None

    def get_user(self, user_id):

        try:
            return User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return None


