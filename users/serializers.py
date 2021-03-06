from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from users.helpers import validate_id_token
from .models import (
    User,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'full_name',
            'phone_number',
            'is_active',
            'profile_picture',
            'gender',
            'push_notification',
            'firebase_uuid',
        )
        read_only_fields = (
            'email',
            'is_active',
            'push_notification',
            'firebase_uuid',
        )


class UserAuthTokenSerializer(AuthTokenSerializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True,
        required=False
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        required=False
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )
    id_token = serializers.CharField(
        label=_("Access Token"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        required=False,
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        id_token = attrs.get('id_token')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        elif id_token:
            user = validate_id_token(id_token)
            if user is None:
                msg = _('Not a valid firebase token')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserRegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(min_length=8, write_only=True, required=True)
    id_token = serializers.CharField(
        label=_("Access Token"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'full_name',
            'phone_number',
            'id_token',
            'gender',
        )

    def validate(self, attrs):
        id_token = attrs.get('id_token')
        user = validate_id_token(id_token)
        if user is None:
            msg = _('Not a valid firebase token')
            raise serializers.ValidationError(msg, code='authorization')
        user.full_name = attrs['full_name']
        user.save()
        attrs['user'] = user
        return attrs
