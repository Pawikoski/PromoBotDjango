from django.urls import path
import PromoBot.views as views

app_name = 'promobot'

urlpatterns = [
    path('', views.index, name="promobot_index"),
    path('get-data/', views.get_data, name="promobot_get_data"),
    path('add-products/', views.add_products, name="promobot_add_products"),
    path('update/', views.update_product, name='update'),
    path('available_categories/<int:store_id>', views.available_categories, name='available_categories'),
]

