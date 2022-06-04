from django.urls import path
import PromoBot.views as views

app_name = 'promobot'

urlpatterns = [
    path('', views.index, name="promobot_index"),
    path('get-stores', views.get_stores, name="get_stores"),
    path('get-categories/<int:store_id>', views.get_categories, name="get_categories"),
    path('get-category-url-and-products/<int:store_id>/<int:category_id>', views.get_category_url_and_products, name="get_category_url_and_products"),
    path('search-best-price', views.search_best_price, name="search_best_price"),
    path('add-product-to-promo/', views.add_product_to_promo, name="add_product_to_promo"),
    
    path('add-products/', views.add_products, name="promobot_add_products"),
    path('update/', views.update_product, name='update'),
    path('available_categories/<int:store_id>', views.available_categories, name='available_categories'),
]

