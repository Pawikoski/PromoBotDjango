from django.contrib import admin
from django.db.models import Count
from .models import Store, UserData, ProductUrls, Product, Version, ProductStat, StoreCategory
import PromoBot.models as pbm

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

admin.site.register(pbm.Store)


class StoresFilter(admin.SimpleListFilter):
    title = 'Store'
    parameter_name = 'store'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        return [(i, f"{store} ({count_store})") for i, store, count_store in qs.values_list('store__id', 'store__name').annotate(user_count=Count('store')).distinct().order_by('store__name')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(store__id=self.value())


class CategoryFilter(admin.SimpleListFilter):
    title = "Category"
    parameter_name = 'category'
    
    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        if 'store' in request.GET.keys():
            store_id = request.GET['store']
            qs = model_admin.get_queryset(request).filter(store__id=store_id)
            
        return [(i, f"{category} ({count_category})") for i, category, count_category in qs.values_list('category__id', 'category__name').annotate(user_count=Count('category')).distinct().order_by('category__name')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__id=self.value())


@admin.register(pbm.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'category', 'price', 'best_price')
    list_filter = (StoresFilter, CategoryFilter)



@admin.register(pbm.StoreCategoryURL)
class StoreCategoryURLAdmin(admin.ModelAdmin):
    
    list_display = ("category", "store", "url")
    list_filter = (StoresFilter, 'category')


@admin.register(pbm.StoreCategory)
class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'stores')
    
    def stores(self, obj):
        return f"{obj.available_stores.all().count()} / {pbm.Store.objects.all().count()}" 


@admin.register(pbm.Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    list_display = ('product', 'store')
    def store(self, obj):
        return obj.product.store.name


@admin.register(pbm.Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'certain')
    readonly_fields = ('product', )
    
    def product_name(self, obj):
        return f"{obj.product.name}"
    
    def price(self, obj):
        return f"{obj.product.price}"