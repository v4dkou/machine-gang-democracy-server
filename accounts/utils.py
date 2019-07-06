import uuid
from random import randint


def generate_password_recovery_code():
    return str(uuid.uuid4())[-8:]


def generate_session_token():
    return str(uuid.uuid4()).replace('-', '')


def generate_confirmation_code():
    return str(randint(1000, 9999))


def get_client_ip(request):
    if not request:
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_user_agent(request):
    return request.META['HTTP_USER_AGENT']


def hide_username(username):
    if not username:
        return username

    chunks = username.split('@')
    x = chunks[0]
    if len(x) > 5:
        x = x[:2] + "*" * max(0, len(x) - 4) + x[-2:]
    elif len(x) > 2:
        x = x[0] + "*" * max(0, len(x) - 1)
    else:
        x = "*" * len(x)
    chunks[0] = x
    return "@".join(chunks)
