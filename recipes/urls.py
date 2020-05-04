from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', landing, name='landing'), # landing page
    path('home/', home, name='home'), # logged in home page
    path('home/search/', homesearch, name='homesearch'), # home search
    path('recipes/', recipes, name='myrecipes'), # recipes
    path('recipes/add/', addrecipes, name='addrecipes'), # add receipe view
    path('recipes/view/<int:id>/', viewrecipes, name='viewrecipes'), # view single recipe
    path('recipes/del/<int:id>/', delrecipes, name='delrecipes'), # deleting selected recipe
    path('recipes/edit/<int:pk>/', edit, name='edit'), # deleting selected recipe

    path('grocery/', mygrocery, name='mygrocery'), # represent all the recipes of logged in user
    path('grocery/list/', grocerylist, name='grocerylist'), # show grocery items of selected recipes in above link.
    path('grocery/view/<int:id>/', viewgrocery, name='viewgrocery'), # view selected grocery
    path('grocery/search/', grocerysearch, name='grocerysearch'), # search for grocery ( recipe)
    path('grocery/add/<int:id>/', groceryadd, name='groceryadd'), # adding grocery view
    path('grocery/del/<int:id>/', delgrocery, name='delgrocery'), # deleting grocery

    path('planner/', planner, name='planner'), # planner home page
    path('planner/add/', addplanner, name='addplanner'), # adding planner page

    path('ourstory/', ourstory, name='ourstory'), # static page
    path('ourpatners/', ourpatners, name='ourpatners'), # static page
    path('news/', news, name='news'), # static page
    path('news1/', news1, name='news1'), # static page
    path('news2/', news2, name='news2'), # static page
    path('contactus/', contactus, name='contactus'), # static page
]
