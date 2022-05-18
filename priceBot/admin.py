from django.contrib import admin
from .models import Store, UserData, ProductUrls, Product, Version, ProductStat

# Register your models here.
admin.site.register(Store)
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

