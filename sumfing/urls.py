from django.contrib import admin
from django.urls import path
from sumfing import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sumfing/', views.sumfing, name = "sumfing"),
    path('next_puzzle/', views.next_puzzle, name = "next_puzzle"),
    path('completed/', views.completed, name = "completed"),    
]
