from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('tasks', views.tasks),
    path('post', views.post),
    path('logout', views.logout),
    path('delete/<int:id>', views.delete),
    path('showtask/<int:id>', views.showtask),
    path('thoughts', views.thoughts),
]