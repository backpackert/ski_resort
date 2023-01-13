import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import RegisteredUser


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'  #156 от 14.10.22 (25 мин)

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).decode('utf-8')

        #auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        auth_header_token = auth_header.split(" ")
        if len(auth_header_token) < 2:
            return None
        auth_header_token = auth_header_token[1]
        token = auth_header_token # 'это не нужно
        return self._authenticate_credentials(request, token)  # 28 минута


    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except Exception as e:
            msg = f'Authentication error. Impossible to decode token {e} {token=}'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = RegisteredUser.objects.get(pk=payload['id'])
        except RegisteredUser.DoesNotExist:
            msg = 'User not found Пользователь соответствующий данному токену не найден.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'Данный пользователь деактивирован.'
            raise exceptions.AuthenticationFailed(msg)
        print(f'{user=}')
        print(f'{token=}')

        return (user, token)
