# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import *
from .serializers import LoginSerializer,SignupSerializer,RatingSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)

                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'message': 'Login successful.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'message': 'Signup successful.'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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


