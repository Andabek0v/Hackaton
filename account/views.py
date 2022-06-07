
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .serializers import CustomAuthTokenSerializer, RegisterSerializer
from .services.utils import send_activation_code
from .models import CustomUser

class RegisterView(APIView):
    """Класс контроллер отвечающий за регистрацию юзера"""

    def post(self, request):
        """Переопределения метода POST"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_activation_code(user.activate_code, user.email)
            return Response(
                'Successfully signed up!',
                status=status.HTTP_201_CREATED
            )


class ActivateView(APIView):
    """Класс контроллер отвечающий за активацию нового юзера через почту"""

    def get(self, request, activate_code):
        """Переопределение метода GET"""
        user = get_object_or_404(CustomUser, activate_code=activate_code)
        user.is_active = True
        user.activate_code = ''
        user.save()
        return Response(
            'Your account successfully activated!',
            status=status.HTTP_200_OK
        )


class LoginView(ObtainAuthToken):
    """Класс контроллер отвечающий за логгирование"""

    serializer_class = CustomAuthTokenSerializer


class LogoutView(APIView):
    """Класс контроллер отвечающий за выход из аккаунта"""

    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        """Переопределение метода POST"""
        Token.objects.filter(user=request.user).delete()
        return Response(
            'Successfully signed out!', status=status.HTTP_401_UNAUTHORIZED
        )