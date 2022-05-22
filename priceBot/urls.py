from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('rejestracja/', views.register_request, name="register"),
    path('logowanie/', views.login_request, name="login"),
    path('wyloguj/', views.logout_request, name="logout"),
    path('moje-konto/', views.user_page, name="user_page"),
    path('obslugiwane-sklepy/', views.available_stores, name="available_stores"),
    path('o-promobot/', views.about_page, name='about'),
    path('kontakt/', views.contact_page, name='contact'),
    path('zglos-blad/', views.report_bug_page, name='report_bug'),
    path('sledz-produkty/', views.add_products, name='add_products'),
    path('pobierz/', views.download, name='download'),
    
    path('produkt/<int:product_id>', views.product, name='product'),
    
    path('edytuj-produkt/<int:product_id>', views.product_edit, name='product_edit'),
    path('edytuj-kategorie/<int:category_id>', views.category_edit, name='category_edit'),
    
    path('products-for-category/', views.products_for_category, name='products_for_category'),
    
    
    path('moje-konto/premium', views.premium, name='premium'),
    path('mojekonto/premium-ustawienia', views.premium_settings, name='premium_settings'),
    path('moje-konto/kategorie', views.categories_account, name='categories_account'),
    path('moje-konto/produkty', views.products_account, name='products_account'),
    path('moje-konto/twoje-dane', views.data_account, name='data_account'),
    path('moje-konto/usun', views.delete_account, name='delete_account'),
]
