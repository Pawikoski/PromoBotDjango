from django.contrib import admin
from .models import Store, UserData, ProductUrls, Product

# Register your models here.
admin.site.register(Store)
admin.site.register(UserData)
admin.site.register(ProductUrls)
admin.site.register(Product)