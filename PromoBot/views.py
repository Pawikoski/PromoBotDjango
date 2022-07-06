from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from PromoBot.models import Store, StoreCategory, Product, StoreCategoryURL, Thumbnail, Promo
import json
import datetime
import os
from django.core.exceptions import ObjectDoesNotExist

from priceBot.models import Category

from rest_framework import viewsets, permissions, authentication
from .serializers import ProductSerializer, PromoSerializer, StoreSerializer, StoreCategorySeralizer, ThumbnailSeralizer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ListStores(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListCategories(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get_store_object(self, store_id):
        try:
            return Store.objects.get(id=store_id)
        except Category.DoesNotExist:
            raise Http404

    def get_categories_objects(self, store_obj):
        try:
            return StoreCategory.objects.filter(available_stores=store_obj)
        except StoreCategory.DoesNotExist:
            raise Http404

    def get(self, request, store_id, format=None):
        store = self.get_store_object(store_id=store_id)
        categories = self.get_categories_objects(store_obj=store)
        serializer = StoreCategorySeralizer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDetails(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    def get_store_object(self, store_id):
        try:
            return Store.objects.get(id=store_id)
        except Category.DoesNotExist:
            raise Http404

    def get_category_object(self, category_id):
        try:
            return StoreCategory.objects.get(id=category_id)
        except StoreCategory.DoesNotExist:
            raise Http404

    def get(self, request, store_id, category_id):
        store_obj = self.get_store_object(store_id)
        category_obj = self.get_category_object(category_id)
        category_url = StoreCategoryURL.objects.get(
            store=store_obj, category=category_obj).url

        products = Product.objects.filter(store=store_obj, category=category_obj)
        serializer = ProductSerializer(products, many=True)

        return Response({"category_url": category_url, "store_name": store_obj.name, "products": serializer.data}, status=status.HTTP_200_OK)


# def get_category_url_and_products(request, store_id, category_id):
    # products_data = dict()

    # store_obj = Store.objects.get(id=store_id)
    # category_obj = StoreCategory.objects.get(id=category_id)

    # category_url = StoreCategoryURL.objects.get(
    #     store=store_obj, category=category_obj).url

    # products = Product.objects.filter(store=store_obj, category=category_obj)
    # products_data[store_obj.name] = {}

    # for product in products:
    #     products_data[store_obj.name].update({
    #         product.url: {
    #             "name": product.name,
    #             "price": product.price,
    #             "last_price": product.last_price,
    #             "best_price": product.best_price,
    #             "best_price_date": product.best_price_date,
    #         }
    #     })

    # return JsonResponse({"url": category_url, "products": products_data})


class Products(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get_store_object(self, store_name):
        try:
            return Store.objects.get(name=store_name)
        except Store.DoesNotExist:
            raise Http404
        
    def get_category_object(self, category_name, store_obj):
        try:
            return StoreCategory.objects.get(available_stores=store_obj, name=category_name)
        except StoreCategory.DoesNotExist:
            raise Http404
        
    def get_product_object(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise Http404
        
    def thumbnails(self, thumbnails_raw):
        thumbnails = [
        {
            "product": Product.objects.get(url = thumb['product_url']).id,
            "img_url": thumb["thumbnail"]
        } for thumb in thumbnails_raw]
        
        thumbnail_serializer = ThumbnailSeralizer(data=thumbnails, many=True)
        if thumbnail_serializer.is_valid():
            thumbnail_serializer.save()
            return True
        
        return False
        
    def post(self, request, product_id=None):        
        store = self.get_store_object(request.data['store_name'])
        store_category = self.get_category_object(request.data['store_category'], store)
        
        products = []
        thumbnails_raw = []
        for product in request.data['products']:
            products.append(
                {
                    "name": product['name'],
                    "store": store.id,
                    "category": store_category.id,
                    "url": product['url'],
                    "price": product['price'],
                    "last_price": None,
                    "best_price": None,
                    "best_price_date": None,
                    "available": product["available"]
                }
            )
            thumbnails_raw.append(
                {
                    "product_url": product['url'],
                    "thumbnail": product["img"],
                }
            )
        
        product_serializer = ProductSerializer(data=products, many=True)
        if product_serializer.is_valid():
            product_serializer.save()
            
            if self.thumbnails(thumbnails_raw):
                return Response({"status": "Successfully added (products, thumbnails)"}, status=status.HTTP_200_OK)
                        
            return Response({"status": "No thumbnails added"}, status=status.HTTP_201_CREATED)
        
        print(product_serializer.errors)
        return Response(data=product_serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, product_id):
        product_to_update = request.data['product_to_update']
        
        product = self.get_product_object(product_id)
        
        available = product_to_update['available']
        name = product_to_update['name']
        price = product_to_update['price']

        db_name = product.name
        db_price = product.price
        db_best_price = product.best_price

        product.last_price = db_price
        product.available = available
        product.price = price
        
        return_data = {}
        if price and db_best_price and float(price) < (db_best_price):
            return_data = {"last_best_price": db_best_price}
            product.best_price = price
            product.price = price
            product.best_price_date = datetime.date.today().strftime("%Y-%m-%d")

        if name != db_name:
            product.name = name
            
        product.save()
        return Response(return_data, status=status.HTTP_200_OK)

    def get(self, request, product_id=None):
        product_name = request.data['product_name']
        store_name = request.data['store_name']
        category_name = request.data['category_name']
        store = Store.objects.get(name__iexact=store_name)
        category = StoreCategory.objects.get(name__iexact=category_name)
        
        product = Product.objects.filter(name__icontains=product_name, category=category).order_by(
        'price', 'name').exclude(price__isnull=True).first()

        lowest = product.price

        return Response({
            "lowest_price": lowest
        }, status=status.HTTP_200_OK)


class Promo(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get_store_object(self, store_name):
        try:
            return Store.objects.get(name=store_name)
        except Store.DoesNotExist:
            raise Http404
    
    def get_category_object(self, category_name):
        try:
            return Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise Http404
        
    def get_product_obj(self, url, store_obj, category_obj):
        try:
            return Product.objects.get(url=url, store=store_obj, category=category_obj)
        except Product.DoesNotExist:
            raise Http404
        
    def post(self, request):
        url = request.data['url']
        store = self.get_store_object(request.data['store_name'])
        category = self.get_category_object(category_name=request.data['category_name'])
        certain = request.data['certain']
        
        product = self.get_product_obj(url=url, store_obj=store, category_obj=category)
        
        serializer = PromoSerializer({"product": product, "certain": certain})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('fail', status=status.HTTP_400_BAD_REQUEST)
        


    



# @csrf_exempt
# def update_product(request):
#     return_data = None

#     data = json.loads(request.body)
#     product_to_update = data['product_to_update']
#     available = product_to_update['available']
#     url = product_to_update['url']
#     name = product_to_update['name']
#     price = product_to_update['price']

#     db_product = Product.objects.get(url=url)
#     db_name = db_product.name
#     db_price = db_product.price
#     db_best_price = db_product.best_price

#     db_product.last_price = db_price
#     db_product.available = available
#     if price and db_best_price and float(price) < (db_best_price):
#         return_data = {"last_best_price": db_best_price}
#         db_product.best_price = price
#         db_product.price = price
#         db_product.best_price_date = datetime.date.today().strftime("%Y-%m-%d")

#     db_product.price = price

#     if name != db_name:
#         db_product.name = name

#     db_product.save()

#     if return_data:
#         return JsonResponse(return_data)
#     else:
#         return JsonResponse({"success": "Product updated."})


# def lowest_price(request):
#     return


def available_categories(request, store_id):
    store = Store.objects.get(id=store_id)
    used_categories = [
        qs.category.id for qs in StoreCategoryURL.objects.filter(store=store)]

    return JsonResponse({'used_categories': used_categories})




