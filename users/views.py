from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from users.serializers import LoginSerializer
from django.contrib.auth import authenticate, login, logout

class LoginView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self, request):
        additional_info = {
            'message': 'This is the login endpoint.',
            'details': 'You can use POST method to login the user.',
            'important_note': 'Do not expose this endpoint to the public. It should be used only internally by the front-end application.',
            'fields': 'username, password'
        }
        return Response(additional_info)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']       

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Successfully logged in!'})
        else:
            return Response({'error': 'Invalid credentials. Login failed.'}, status=400)


class LogoutView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        additional_info = {
            'message': 'This is the logout endpoint.',
            'details': 'You can use POST method to logout the user.',
            'important_note': 'Do not expose this endpoint to the public. It should be used only internally by the front-end application.',
            'fields': 'username'
        }
        return Response(additional_info)
    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out!'})
    
    
