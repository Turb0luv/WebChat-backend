from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.db.models.functions import datetime
from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     # validators=[validate_password]
                                     )
    confirmation_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirmation_password')

    def create(self, validated_data):
        if validated_data['password'] != validated_data[
                                                    'confirmation_password']:
            raise serializers.ValidationError(
                {"confirmation_password": ["Пароли не совпадают"]})
        else:
            user = User.objects.create_user(username=validated_data['username'],
                                            password=validated_data['password'])
            user.save()
            return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        if data['username'] is None or data['password'] is None:
            raise serializers.ValidationError(
                {'username': 'Это поле обязательно.',
                 'password': 'Это поле обязательно.'}
            )
        if User.objects.get(username=data['username']).check_password(
                data['password']):
            token = Token.objects.get_or_create(
                user=User.objects.get(username=data['username']))
            data = {'user': {'name': data['username'],
                             'id': User.objects.get(
                                 username=data['username']).id},
                    'token': str(token[0])}
            return data
        else:
            raise serializers.ValidationError(
                {'username': 'Логин или пароль неверны'}
            )

