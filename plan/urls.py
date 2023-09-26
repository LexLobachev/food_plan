from django.urls import path

from .views import *


app_name = "plan"

urlpatterns = [
    path('', index, name='home'),
    ]
