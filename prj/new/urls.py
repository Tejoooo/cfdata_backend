
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('ratinglist/',RatingView.as_view(),name='ratinglist'),
    path('ratingdelete/<str:name>/',RatingDelete.as_view(),name='ratingdelete'),
]
