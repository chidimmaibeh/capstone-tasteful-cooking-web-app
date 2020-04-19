from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(Recipe)
admin.site.register(Grocery)
admin.site.register(Planner)
