from atexit import register
from django.contrib import admin
from .models import Categories, Products, UserCart

# Register your models here.

admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(UserCart)