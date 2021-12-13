from .models import User


def checkAuth(username, password):
    user = User.objects.get(username=username)
    return user.is_password_correct(password)
