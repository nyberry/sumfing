from django.contrib import admin
from django.urls import path
from numbler import views

urlpatterns = [
    path('', views.numbler, name='numbler'),
    path('numbler/', views.numbler, name = "numbler"),
    path('next_puzzle/', views.next_puzzle, name = "next_puzzle"),    
]
