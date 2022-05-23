from django.urls import path
import PromoBot.views as views

urlpatterns = [
    path('', views.index, name="promobot_index"),
    path('get-data/', views.get_data, name="promobot_get_data"),
    path('add-products/', views.add_products, name="promobot_add_products"),
]

