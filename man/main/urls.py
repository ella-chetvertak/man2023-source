from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('often', views.often, name='often'),
    path('search', views.search, name='search'),
    path('nltk_ton', views.nltk_ton, name='nltk_ton'),
    path('settings', views.settings, name='settings'),
    path('reset_settings', views.reset_settings, name='reset_settings'),
    path('about', views.about, name='about'),
]
