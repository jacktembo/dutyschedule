from django.urls import path, include
from django.contrib import admin
from .import views

app_name = 'accounts'
urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('password-change', views.change_password, name='password-change'),
    path('password-reset', views.password_reset, name='password-reset'),
    path('password-reset/confirm/<str:email>',
         views.password_reset_confirm, name='password-reset-confirm'),
    

]
