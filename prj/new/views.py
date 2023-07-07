# views.py

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status,generics
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from .models import *
from .serializers import LoginSerializer,SignupSerializer,RatingSerializer,UserSerializer


class LoginView(generics.GenericAPIView):
    def post(self,request:Request):
        email = request.data['email']
        password = request.data['password']
        try:
            user = User.objects.get(email=email)
            if user is not None and check_password(password, user.password):
                token_obj,_ = Token.objects.get_or_create(user=user)
                response = {
                    "message" : "Login Succesfully",
                    "token" : token_obj.key
                }
                return Response(data=response,status=status.HTTP_200_OK)
            else:
                response = {
                    "error" : "Login Credentials doesn't matched"
                }
                return Response(data=response,status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            response = {
                "error" : "User Doesn't exist"
            }
            return Response(data=response,status=status.HTTP_404_NOT_FOUND)


class SignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self,request:Request):
        data = request.data
        username = data['username']
        email = data['email']
        username_exits = User.objects.filter(username=username).exists()
        if username_exits:
            response = {
                "username":"UserName Already exits"
            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)

        email_exits = User.objects.filter(email=email).exists()
        if email_exits:
            response = {
                "email":"Email Already exits"
            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)


        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user =serializer.save()
            token_obj,_ = Token.objects.get_or_create(user=user)
            response = {
                "message":"User Created Succesfully",
                "data":serializer.data,
                "token":token_obj.key
            }

            return Response(data=response,status=status.HTTP_200_OK)
        else:
            response = {
                "error":"Error occured"
            }
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)



class RatingView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class RatingDelete(generics.DestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    lookup_field = 'name'  # Change the lookup field to 'name' for filtering by name

    def get_queryset(self):
        # Optionally, you can filter the queryset based on some condition if needed
        queryset = super().get_queryset()
        # Example: Filtering ratings based on a user or any other condition
        user = self.request.query_params.get('user', None)
        if user:
            queryset = queryset.filter(user__username=user)
        return queryset

    def delete(self, request, *args, **kwargs):
        name = kwargs.get('name')
        try:
            rating = Rating.objects.get(username=name)
            self.perform_destroy(rating)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Rating.DoesNotExist:
            return Response({'error': 'Rating not found.'}, status=status.HTTP_404_NOT_FOUND)


