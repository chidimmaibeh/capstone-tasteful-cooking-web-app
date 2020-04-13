from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', landing, name='landing'),
    path('home/', home, name='home'), # logged in home page
    path('recipes/', recipes, name='myrecipes'),
    path('recipes/add/', addrecipes, name='addrecipes'),
    path('recipes/view/<int:id>/', viewrecipes, name='viewrecipes'),

    path('ourstory/', ourstory, name='ourstory'),
    path('ourpatners/', ourpatners, name='ourpatners'),
    path('news/', news, name='news'),
    path('news1/', news1, name='news1'),
    path('news2/', news2, name='news2'),
    path('contactus/', contactus, name='contactus'),
]
