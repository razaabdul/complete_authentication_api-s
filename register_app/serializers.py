from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from .models import *
from rest_framework.response import Response
from datetime import datetime


User=get_user_model()

class RegisterationSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
   
    class Meta:
        model=User
        fields="__all__"
        extra_kwargs={"password":{"write_only":True}}

    def create(self,validated_data):
        email=validated_data.pop("email")
        password=validated_data.pop("password")
        user=User.objects.create_user(
        email=email,
        password=password,
        **validated_data)
        print(user.password)
        refresh=RefreshToken.for_user(user)
        access_token=str(refresh.access_token)

        expires_in_timestamp = refresh.access_token.payload["exp"]
        expires_in_datetime = datetime.fromtimestamp(expires_in_timestamp)
        expires_in_seconds = int((expires_in_datetime - datetime.now()).total_seconds())

        return {
            "user":user,
            "refresh_token":str(refresh),
            "access_token":access_token,
            "expire_in":expires_in_seconds
        }

class UserLogin(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    def validate(self,data):
        email=data.get("email")
        password=data.get("password")
        user=User.objects.filter(email=email).first()
        if user is None:
            raise  serializers.ValidationError("user not found")
        if not user.check_password(password):
            raise serializers.ValidationError("invalid password")
        refresh=RefreshToken.for_user(user)
        access_token=str(refresh.access_token)
        expires_in_timestamp = refresh.access_token.payload["exp"]
        expires_in_timestamp=datetime.fromtimestamp(expires_in_timestamp)
        expire_in_second=int((expires_in_timestamp - datetime.now()).total_seconds())

        return  {
            "user":user.id,
            "access_token":access_token,
            "expire_in":expire_in_second,
            "type":user.user_type
        }

