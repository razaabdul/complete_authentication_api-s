from . serializers import *
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from rest_framework import status
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings
# from django.contrib.auth.hashers import make_password
import random
from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException
import string
from django.contrib.auth.hashers import make_password

# Create your views here.
User=get_user_model()
class Userview(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class=RegisterationSerializer

    @action(detail=False,methods=["POST"],url_path="register")
    def register(self,request):
        try:
            data=request.data
            print('data: ', data)
            serializer=RegisterationSerializer(data=request.data)
            if serializer.is_valid():
                # hash=make_password(data["password"])
                if User.objects.filter(email=request.data.get('email')).exists():
                    return Response({"message":"email already exists"},
                                    400,"bad request")
                serializer.save()
                return Response({"message":"user added successfully"},200)
            return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"An error occured:{str(e)}")      
            return Response({"message":"An unexpected  error occurred"},status=status.HTTP_400_BAD_REQUEST)
        

    @action (detail=False ,methods=["POST"],url_path="login")   
    def login(self,request):
        email=request.data.get("email").lower()
        try:
            email= User.objects.get(email=email)
            
        except Exception as e:
            return Response({"message":"Invalid Credentails"},status=status.HTTP_400_BAD_REQUEST)
    
        try :
            serializer=UserLogin(data=request.data)
    
            if serializer.is_valid():
                response=serializer.validated_data
                return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message":"an unexpected error occured"})
    
        return Response(serializer.errors)
    @action (detail=False,methods=["POST"],url_path="send-otp")
    def sent_otp(self,request):
        email=request.data.get("email")
        try:
            user=User.objects.get(email=email)
        except Exception as e:
            return Response({"message":"you are not registered user "},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            otp="".join([str(random.randint(0, 9)) for _ in range(4)])
         
            a=OTP.objects.update_or_create(email=email,defaults={"otp":otp})
        
            send_mail(  
                "password reset otp",
                f"your otp for password reset is:{otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
            return Response(
                {"message":"OTP sent successfully "},status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error":str(e),"message":"something went wrong"},status=status.HTTP_400_BAD_REQUEST
            )
    @action(detail=False,methods=["POST"],url_path="otp-verify")
    def verify_otp(self,request):
        try:
            email=request.data.get("email")
            otp=request.data.get("otp")
            if not email or not otp:
                raise APIException ("Email or otp are required")
            obj=OTP.objects.filter(email=email,otp=otp).first()
            if obj:
                token= "" .join(random.choices(string.ascii_uppercase + string.digits, k=12))
                obj.token=token
                obj.otp=""
                obj.save()
                return Response({"message":"OTP verified successfully .", "token":token,},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Invalid OTP"},status=status.HTTP_400_BAD_REQUEST)   
        except Exception as e:
            return Response(
                {"message":"Failed to generate OPT .please try again later."},status=status.HTTP_400_BAD_REQUEST
            )    
    @action(detail=False,methods=["POST"],url_path="reset-password")
    def reset_password(self,request):
        try:
            email=request.data.get("email") 
            new_password=request.data.get("new_password")
            token=request.headers.get("Authorization")
            if not email or not new_password:
                raise APIException("Email and New Password are required")
            obj=OTP.objects.filter(email=email,token=token).first()
            if obj:
                user=User.objects.get(email=email)
                print(user)
                user.password=make_password(new_password) 
                print(user.password)
                user.save()
                obj.delete() 
                return Response({"message":"Password reset successfully."}
                ) 
            else:
                return Response({"message":"Failed to reset password"},status=status.HTTP_400_BAD_REQUEST)   
        except Exception as e:
            return Response({"message":"Failed to reset password user not found !"},status=status.HTTP_400_BAD_REQUEST)        
        

