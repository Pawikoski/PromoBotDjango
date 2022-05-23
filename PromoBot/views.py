from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from PromoBot.models import Store, StoreCategory, Product
import json
import datetime
import os



# Create your views here.

def verify_ip(view):
    def wrapper(request):
        if request.META['REMOTE_ADDR'] != os.environ.get('REQUIRED_IP'):
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
        categories = StoreCategory.objects.filter(store=store)
        stores_data[store.name] = {"urls": [(category.name, category.url) for category in categories]}
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
@verify_ip
def add_products(request):
    if request.method != "POST":
        return JsonResponse({"halo": "widzisz mnie???"})
    
    data = json.loads(request.body)
    products = data['products']
    store_name = data['store_name']
    store_category_name = data['store_category']
    print(products)
    
    store = Store.objects.get(name=store_name)
    store_category = StoreCategory.objects.get(store=store, name=store_category_name)
    
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
