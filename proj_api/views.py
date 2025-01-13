from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

JWT_AUTH_COOKIE = settings.REST_AUTH.get('JWT_AUTH_COOKIE', 'my-app-auth')
JWT_AUTH_REFRESH_COOKIE = settings.REST_AUTH.get('JWT_AUTH_REFRESH_COOKIE', 'my-refresh-token')
JWT_AUTH_SAMESITE = getattr(settings, 'JWT_AUTH_SAMESITE', 'None')
JWT_AUTH_SECURE = getattr(settings, 'JWT_AUTH_SECURE', True)


@api_view()
def root_route(request):
    return Response({
        "message": "Welcome to my drf API!"
    })


@api_view(['POST'])
def logout_route(request):
    response = Response()
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response