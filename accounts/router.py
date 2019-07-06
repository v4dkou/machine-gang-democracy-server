from . import viewsets as v
from . import jwt_views as jwt_v


def register(router):
    router.register('jwt-login', jwt_v.ObtainJSONWebToken, 'jwt-login')
    router.register('jwt-refresh', jwt_v.RefreshJSONWebToken, 'jwt-refresh')
    router.register('refresh-token/refresh', jwt_v.RefreshTokenViewSet, 'refresh-token-refresh')
    router.register('refresh-token/logout', jwt_v.LogoutViewSet, 'refresh-token-logout')

    router.register('users', v.UserViewSet, base_name='users')
