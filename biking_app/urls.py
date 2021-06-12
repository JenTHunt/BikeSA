from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index),
    path('register', views.register),
    path('register_biker', views.register_biker),
    path('login', views.login),
    path('welcome', views.welcome),
    path('log_ride', views.log_ride),
    path('logout', views.logout),
    path('newsfeed', views.newsfeed),
    path('create_post', views.create_post),
    path('add_comment/<int:id>', views.add_comment),
    path('like/<int:id>', views.like),
    path('rides/<int:id>/delete', views.delete),
    path('rides/<int:id>/edit', views.edit),
    path('posts/<int:id>/delete', views.delete_post),
    path('comments/<int:id>/delete', views.delete_comment),
]