from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from PromoBot.models import Store, StoreCategory, Product, StoreCategoryURL
import json
import datetime
import os
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.

def verify_ip(view):
    def wrapper(request):
        if request.META['REMOTE_ADDR'] != os.environ.get('REQUIRED_IP'):
            return redirect('main:homepage')
        
        return view(request)
    return wrapper


def only_post_method(view):
    def wrapper(request):
        if request.method != "POST":
            return redirect('main:homepage')
        return view(request)
    return wrapper

    

@verify_ip
def index(request):
    
    print(os.environ)
    return HttpResponse('sdf')

@verify_ip
def get_data(request):
    stores_data = dict()
    products_data = dict()
    
    stores = Store.objects.all()
    for store in stores:
        categories = StoreCategory.objects.filter(available_stores=store)
        stores_data[store.name] = {"urls": []}
        for category in categories:
            try:
                url_obj = StoreCategoryURL.objects.get(store=store, category=category)
                stores_data[store.name]['urls'].append((url_obj.category.name, url_obj.url))
            except ObjectDoesNotExist:
                pass
                
        
        products = Product.objects.filter(store=store)
        products_data[store.name] = {}
        
        for product in products:
            products_data[store.name].update({
                product.url: {
                    "name": product.name,
                    "price": product.price,
                    "last_price": product.last_price,
                    "best_price": product.best_price,
                    "best_price_date": product.best_price_date,
                    }
                })
    

    data = {
        "stores": stores_data,
        "products": products_data
    }
    
    return JsonResponse(data) 


@csrf_exempt
def add_products(request):
    data = json.loads(request.body)
    products = data['products']
    store_name = data['store_name']
    store_category_name = data['store_category']
    
    store = Store.objects.get(name=store_name)
    store_category = StoreCategory.objects.get(available_stores=store, name=store_category_name)
    
    for product in products:
        if Product.objects.filter(url=product['url']):
            print('obj exists, compare prices etc.')
            continue
        new_product = Product(
            name = product['name'],
            store = store,
            category = store_category,
            url = product['url'],
            price = product['price'],
            last_price = product['price'],
            best_price = product['price'],
            best_price_date = datetime.date.today().strftime("%Y-%m-%d")
        )
        new_product.save()
    
    
    return JsonResponse({"szef": data})


@csrf_exempt
def update_product(request):
    return_data = None
    
    data = json.loads(request.body)
    product_to_update = data['product_to_update']
    available = product_to_update['available']
    url = product_to_update['url']
    name = product_to_update['name']
    price = product_to_update['price']
    
    db_product = Product.objects.get(url=url)
    db_name = db_product.name
    db_price = db_product.price
    db_best_price = db_product.best_price
    
    db_product.last_price = db_price
    db_product.available = available
    if price and db_best_price and float(price) < (db_best_price):
        return_data = {"last_best_price": db_best_price}
        db_product.best_price = price
        db_product.price = price
        db_product.best_price_date = datetime.date.today().strftime("%Y-%m-%d")
        
    db_product.price = price
        
    if name != db_name:
        db_product.name = name
        
    db_product.save()
    
    if return_data:
        return JsonResponse(return_data)
    else:
        return JsonResponse({"success": "Product updated."})
    

def lowest_price(request):
    return
