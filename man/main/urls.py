from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('often', views.often, name='often'),
    path('search', views.search, name='search'),
    path('nltk_ton', views.nltk_ton, name='nltk_ton'),
]