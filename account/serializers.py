from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    """
    Класс отвечающий за сериализацию, дисериализацию и валидацию регистрации
    """

    password_confirm = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        """Класс для дополнительной информации"""
        model = CustomUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        """
        Метод для проверки паролей на схожесть
        Срабатывает когда будет вызыватся метод .is_valid()
        """
        password = validated_data.get('password')
        password_confirm = validated_data.pop('password_confirm')

        if len(password) < 8 or len(password_confirm) < 8:
            raise serializers.ValidationError('The password less then 8 char!')
        if password != password_confirm:
            raise serializers.ValidationError("The passwords do not match!")
        return validated_data

    def create(self, validated_data):
        """
        Данный метод вызывается когда будет вызван метод self.save()
        """
        return CustomUser.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    """
    Класс отвечающий за валидацию данных при логгировании
    """

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        """Метод для проверки данных на существование юзера"""
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )
            if not user:
                message = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = 'Must include "email" and "password".'
            raise serializers.ValidationError(message, code='authorization')
        attrs['user'] = user
        return attrs