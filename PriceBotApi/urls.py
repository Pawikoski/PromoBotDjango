from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('auth/', views.auth, name='auth'),
    path('version/', views.version, name='version'),
    path('get_data/', views.get_data, name="get_data"),
    path('product_stats', views.product_stats, name='stats')
]