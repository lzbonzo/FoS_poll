from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class TokenCheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_request(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        content = {"message": "user not auth"}
        user_token = Token.objects.get(user=request.user)
        if token and token == user_token:
            return None
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)
