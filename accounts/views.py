from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser


class AuthCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({
            'id': request.user.id,
            'isAuthenticated': True,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'groups': request.user.groups.values_list('name', flat=True),
        })


class CSRFTokenView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return JsonResponse({"csrfToken": get_token(request)})

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            login(request, user)
            return JsonResponse({'message': 'Logged in successfully'})
        return JsonResponse({'message': 'Invalid credentials'}, status=400)
    
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})