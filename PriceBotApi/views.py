import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from priceBot.models import UserData, Product, ProductUrls, Version
from django.core.exceptions import ObjectDoesNotExist
# TODO: Refator to DRF


# Create your views here.
def verify(request):
    print(request.POST)
    


def main(request):
    return JsonResponse({"error": "Please provide an endpoint"})


def version(request):
    version = Version.objects.first().version
    print(version)
    return JsonResponse({"version": version})


def auth(request):
    if 'Version' not in request.headers.keys() or request.headers['Version'] != Version.objects.first().version:
        return JsonResponse({"error": "Invalid version"})
    # TODO: last api call > save datetime to model
    try:
        token = bytes(request.headers['Token'].encode("ascii"))
        user_data = UserData.objects.get(token=token)
        user = user_data.user
        # TODO: user settingslike premium, time breaks etc.
        
        user_data_dict = {
            "telegram_api_key": user_data.telegram_api_key,
            "telegram_user_id": user_data.telegram_user_id,
            "phone_number": str(user_data.phone_number),
        }
        
        products_obj = Product.objects.filter(user=user)
        products = []
        for prod in products_obj:
            product_settings = {
                "wanted_price": prod.wanted_price,
                "wanted_price_tolerancy": prod.wanted_price_tolerance,
                "wanted_price_notifications": json.loads(prod.wanted_price_notifications),
                "lowest_price_notification_time_value": prod.lowest_price_notification_time_value,
                "lowest_price_notification_time_unit": prod.lowest_price_notification_time_unit,
                "lowest_price_notifications": json.loads(prod.lowest_price_notifications),
            }
            
            products.append({
                "name": prod.product_name,
                "settings": product_settings                
            })
        
        return JsonResponse({
                "products": products,
                "user_data": user_data_dict,
            })
    except KeyError or ObjectDoesNotExist:
        return JsonResponse({"error": "Please provide valid API KEY"})


@csrf_exempt
def get_data(request):
    if request.method != "POST":
        return HttpResponseNotAllowed('none')
    
    if 'Version' not in request.headers.keys() or request.headers['Version'] != Version.objects.first().version:
        return JsonResponse({"error": "Invalid version"})
        
    # TODO: Catch exceptions
    token = bytes(request.headers['Token'].encode("ascii"))
    user = UserData.objects.get(token=token).user
        
    product_name = request.POST['product_name']
    print(product_name)
    product_obj = Product.objects.get(product_name=product_name, user=user)
    urls = json.loads(ProductUrls.objects.get(product=product_obj).urls)['urls']
    data = urls
    
    return JsonResponse({"data": data})
    
    
    


def product_stats(request):
    if request.method != "POST":
        return HttpResponseNotAllowed('none')
    
    