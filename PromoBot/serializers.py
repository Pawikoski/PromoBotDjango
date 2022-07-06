from .models import Product, Promo, Store, StoreCategory, Thumbnail
from rest_framework import serializers


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "url"]


class StoreCategorySeralizer(serializers.ModelSerializer):
    class Meta:
        model = StoreCategory
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", 'name', 'store', 'category', 'url', 'price', 'last_price',
                  'best_price', 'best_price_date']


class ThumbnailSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Thumbnail
        fields = ['product', 'img_url']
        

class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = ['product', 'certain']