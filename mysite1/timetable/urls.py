from django.urls import path

from . import views

urlpatterns = [
    path('tt/', views.index, name='tt'),
    path('login/', views.login, name='login'),
]