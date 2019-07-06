from rest_framework_jwt.settings import api_settings

from accounts.models import UserSession
from accounts.utils import generate_session_token, get_client_ip, get_client_user_agent


def create_session(user, request):
    return UserSession.objects.create(
        user=user,
        token=generate_session_token(),
        ip_address=get_client_ip(request),
        user_agent=get_client_user_agent(request),
    )

def sign_response_with_refresh_token(user_session, response, is_secure):
    response.set_signed_cookie(
        'HAKATHON_REFRESH_TOKEN',
        user_session.token,
        max_age=None,
        expires=None,
        httponly=True,
        path='/api/v1.0/refresh-token/',
        secure=is_secure,
        samesite='Strict'
    )
