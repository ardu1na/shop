
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.serializers import UserSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        
        # Check if a user with the given username already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_409_CONFLICT)  # HTTP 409 Conflict
        
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})



class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        token = get_object_or_404(Token, user=user)
        token.delete()
        return Response({'message': f'Goodbye, {user.username}!'}, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")