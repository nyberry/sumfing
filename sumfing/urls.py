from django.contrib import admin
from django.urls import path
from sumfing import views

urlpatterns = [
    path('', views.welcome, name='sumfing'),
    path('sumfing/', views.sumfing, name = "sumfing"),
    path('next_puzzle/', views.next_puzzle, name = "next_puzzle"),    
]
