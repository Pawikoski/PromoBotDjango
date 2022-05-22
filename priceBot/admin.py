from django.contrib import admin
from .models import Store, UserData, ProductUrls, Product, Version, ProductStat, StoreCategory

# Register your models here.

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'categories', 'is_premium')
    
    def categories(self, obj):
        return ', '.join([c.name for c in obj.category.all()])
    
admin.site.register(Store, StoreAdmin)


class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(StoreCategory, StoreCategoryAdmin)

admin.site.register(UserData)
admin.site.register(ProductUrls)
admin.site.register(Product)
admin.site.register(ProductStat)

class VersionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if Version.objects.all().count() == 0:
            return True
        return False

admin.site.register(Version, VersionAdmin)

