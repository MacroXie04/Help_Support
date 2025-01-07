from django.contrib.auth.decorators import login_required
from django.utils.decorators import async_only_middleware
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def login(request):
    # get username and password from request
    username = request.data.get('username')
    password = request.data.get('password')

    # authenticate user
    user = authenticate(username=username, password=password)

    # if user is not None, return token
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verification_code(request):






@login_required
@api_view(['POST'])
def logout(request):
    # get token from request
    token_key = request.data.get('token')

    # try to delete token from database
    try:
        token = Token.objects.get(key=token_key)
        token.delete()
        return Response(status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


