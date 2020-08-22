from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #widk logowania
    path('register/', views.register, name='register'),
    #path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name = 'account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'account/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),

]