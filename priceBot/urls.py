from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('rejestracja/', views.register, name="register")
]
