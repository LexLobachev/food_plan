from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views


app_name = "plan"

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/profile/', views.lk, name='lk'),
    ]
