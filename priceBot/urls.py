from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('rejestracja/', views.register_request, name="register"),
    path('logowanie/', views.login_request, name="login"),
    path('wyloguj/', views.logout_request, name="logout")
]
