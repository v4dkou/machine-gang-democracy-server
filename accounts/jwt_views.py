# coding: utf-8
from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt import views as _v
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer
from accounts.models import UserSession
from accounts.jwt_serializers import JSONWebTokenSerializer, RefreshTokenSerializer
from accounts.utils import generate_session_token
from accounts.jwt_utils import create_session, sign_response_with_refresh_token


def jwt_response_payload_handler(token, user, request):
    default_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

    response_data = default_handler(token, user, request)

    response_data['user_id'] = user.id

    return response_data


class ObtainJSONWebToken(_v.ObtainJSONWebToken, ViewSet):
    u"""
    Метод API, который принимает POST с типом аккаунта (email|phone), логином и паролем пользователя.
    Возвращает токен для аутентификации в Hakathon и идентификатор пользователя.
    """
    serializer_class = JSONWebTokenSerializer
    permission_classes = []

    def create(self, *args, **kwargs):
        return self._post(*args, **kwargs)

    def _post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.object.get('user') or request.user
        token = serializer.object.get('token')

        user_session = create_session(user, request)

        response_data = jwt_response_payload_handler(token, user, request)
        response_data['refresh_token'] = user_session.token

        response = Response(response_data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() +
                          api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)

        sign_response_with_refresh_token(user_session, response, request.is_secure())

        return response


class RefreshJSONWebToken(_v.RefreshJSONWebToken, ViewSet):
    u"""
    Метод API, который возвращает обновленный токен для аутентификации
    (с новым expiration) на основании текущего токена
    """
    serializer_class = RefreshJSONWebTokenSerializer
    permission_classes = []

    def create(self, *args, **kwargs):
        return super(_v.RefreshJSONWebToken, self).post(*args, **kwargs)


class RefreshTokenViewSet(ViewSet):
    u"""
    Метод для обновления auth_token используя refresh_token
    """
    authentication_classes = tuple()
    permission_classes = []

    def create(self, request, *args, **kwargs):
        refresh_token = request.get_signed_cookie('HAKATHON_REFRESH_TOKEN', None)

        if not refresh_token:
            serializer = RefreshTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            refresh_token = serializer.validated_data['refresh_token']

        try:
            user_session = UserSession.objects.get(token=refresh_token)
        except UserSession.DoesNotExist:
            response = Response({'refresh_token': 'Refresh token is invalid.'}, status=401)
            response.delete_cookie('HAKATHON_REFRESH_TOKEN')

            return response

        user_session.token = generate_session_token()
        user_session.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user_session.user)
        token = jwt_encode_handler(payload)

        response = Response({
            'token': token,
            'user_id': user_session.user.id,
            'refresh_token': user_session.token
        })

        sign_response_with_refresh_token(user_session, response, request.is_secure())

        return response


class LogoutViewSet(ViewSet):
    u"""
    Метод для закрытия сессии через refresh_token
    """
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        refresh_token = request.get_signed_cookie('HAKATHON_REFRESH_TOKEN', None)

        if not refresh_token:
            serializer = RefreshTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            refresh_token = serializer.validated_data['refresh_token']

        try:
            user_session = UserSession.objects.get(user=request.user, token=refresh_token)
            user_session.delete()
        except UserSession.DoesNotExist:
            pass

        response = Response({}, 200)
        response.delete_cookie('HAKATHON_REFRESH_TOKEN')

        return response
