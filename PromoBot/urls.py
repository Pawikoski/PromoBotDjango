from django.urls import include, path
import PromoBot.views as views

from rest_framework import routers

app_name = 'promobot'

urlpatterns = [
    path('stores/', views.ListStores.as_view()),
    path('categories/<int:store_id>', views.ListCategories.as_view()),
    path('category-details/<int:store_id>/<int:category_id>',
         views.CategoryDetails.as_view()),
    path('products/<int:product_id>', views.Products.as_view()),
    path('products/', views.Products.as_view()),
    path('add-product-to-promo/', views.Promo.as_view()),


    #     path('get-category-url-and-products/<int:store_id>/<int:category_id>',
    #          views.get_category_url_and_products, name="get_category_url_and_products"),


    #     path('search-best-price', views.search_best_price, name="search_best_price"),
    #     path('add-product-to-promo/', views.add_product_to_promo,
    #          name="add_product_to_promo"),

    #     path('add-products/', views.add_products, name="promobot_add_products"),
    #     path('update/', views.update_product, name='update'),
    #     path('available_categories/<int:store_id>',
    path('available-categories/<int:store_id>', views.available_categories, name='available_categories'),
]
