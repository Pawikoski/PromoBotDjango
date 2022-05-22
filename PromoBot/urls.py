from django.urls import path
import PromoBot.views as views

urlpatterns = [
    path('', views.index, name="promobot_index")
]

