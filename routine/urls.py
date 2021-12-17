from django.urls import path, include
from django.contrib import admin
from .import views

app_name = 'routine'

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('today-rota', views.today_rota, name='today-rota'),
    path('announcements', views.annoucements, name='announcements'),
    path('announcement/detail/<int:id>',
         views.announcement_detail, name='announcement-detail'),

]
