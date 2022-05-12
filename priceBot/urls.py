from django.urls import path
from . import views

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
    path('sledz-produkty/', views.add_products, name='add_products')
]
