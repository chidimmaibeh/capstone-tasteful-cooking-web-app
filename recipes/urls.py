from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', landing, name='landing'),
    path('home/', home, name='home'), # logged in home page
    path('recipes/', recipes, name='myrecipes'),
]
