import json
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .forms import NewUserForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Category, ProductUrls, Store, UserData, Download
import uuid
from urllib.parse import urlparse, urlsplit, urlunsplit
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError, ObjectDoesNotExist


# Create your views here.
def homepage(request):
    return render(request, 'app/homepage.html')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Rejstracja przebiegła pomyślnie.")
            return redirect("main:homepage")
        messages.error(request, "Podczas rejestracji wystąpił błąd. Sprawdź podane informacje i spróbuj ponownie")

    form = NewUserForm()
    return render(request, 'app/register.html', {"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Jesteś zalogowany, {username}!")
                return redirect("main:homepage")
            else:
                messages.error(request, "Nieprawidłowa nazwa użytkownika lub hasło")
        else:
            messages.error(request, "Nieprawidłowa nazwa użytkownika lub hasło")

    form = AuthenticationForm()
    return render(request, "app/login.html", {"login_form": form})


def logout_request(request):
    if not request.user.is_authenticated:
        return redirect("main:homepage")
    logout(request)
    messages.info(request, "Zostałeś wylogowany")
    return redirect('main:homepage')


def user_page(request):
    if not request.user.is_authenticated:
        return redirect("main:homepage")

    return render(request, 'account/main.html')


def products_for_category(request):
    print(request.GET)
    user = request.user
    # products = Product.objects.filter
    return JsonResponse({})


def add_products(request):
    if not request.user.is_authenticated:
        return redirect('homepage')
    
    categories = Category.objects.filter(user=request.user)
    print(categories)
    context = {
        "available_categories": categories,
    }
    
    
    if request.method == "POST":
        data = request.POST
        
        if 'form-name' not in data.keys():
            return render(request, "app/add_products.html", {"errors": "Wystąpił niespodziewany błąd"})
        
        match request.POST['form-name']:
            case 'add-product':
                category = data['category']
                product_name = data['product-name']
                
                category_obj = Category.objects.get(category_name=category)
                if Product.objects.filter(category=category_obj, product_name=product_name):
                    return HttpResponse("produkt o tej nazwie juz istnieje")
                
                try:
                    wanted_price = int(data['wanted-price'])
                    if (data['wanted-price-tolerancy']):
                        wanted_price_tolerancy = int(data['wanted-price-tolerancy'])
                    else:
                        wanted_price_tolerancy = 0
                    
                    lowest_price_notification_time_value = int(data['lowest-price-notification-time-value'])
                    lowest_price_notification_time_unit = data['lowest-price-notification-time-unit']
                    
                    if wanted_price < 1 or wanted_price_tolerancy < 0 or wanted_price_tolerancy > 20 or lowest_price_notification_time_unit not in ['m', 'h']:
                        raise ValueError
                except ValueError:
                    return render(request, 'app/add_products.html', context = {"available_categories": categories, "errors": ["Błąd. Sprawdź dane i spróbuj ponownie"]})
                
                main_notification_choices_json = json.dumps({"choices": data.getlist('main-notify')}, indent=4)
                lowest_price_notification_choices_json = json.dumps({"choices": data.getlist('lowest_price_notifty')}, indent=4)
                
                new_product = Product(
                    user = request.user,
                    category = category_obj,
                    product_name = product_name,
                    wanted_price = wanted_price,
                    wanted_price_tolerance = wanted_price_tolerancy,
                    wanted_price_notifications = main_notification_choices_json,
                    lowest_price_notification_time_value = lowest_price_notification_time_value,
                    lowest_price_notification_time_unit = lowest_price_notification_time_unit,
                    lowest_price_notifications = lowest_price_notification_choices_json
                )
                
                new_product.save()
                
                ProductUrls(product=new_product).save()
                
                
        
    return render(request, 'app/add_products.html', context=context)
    

def product_edit(request, product_id):
    if not request.user.is_authenticated:
        return redirect("main:homepage")
    return render(request, 'product/product_edit.html')


def category_edit(request, category_id):
    if not request.user.is_authenticated:
        return redirect("main:homepage")
    return render(request, 'product/category_edit.html')


def categories_account(request):
    if not request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        if 'form-name' not in request.POST.keys():
            return render(request, "account/main.html", {"errors": "Wystąpił niespodziewany błąd"})
    
        match request.POST['form-name']:
            case 'add-category':
                category_name = request.POST['category-name']
                if Category.objects.filter(category_name=category_name, user=request.user):
                    return render(request, 'account/main.html', {"errors": "Kategoria o wybranej nazwie już istnieje"})
                
                new_category = Category(category_name=category_name, user=request.user)
                new_category.save()
                
    categories = [
        {
            "id": category.id,
            "name": category.category_name,
            "products_count": len(Product.objects.filter(category=category, user=request.user))
        } for category in Category.objects.filter(user=request.user)
    ]
    context = {
        "categories": categories
    }
    print(categories)
    return render(request, 'account/categories.html', context=context)


def products_account(request):
    if not request.user.is_authenticated:
        return redirect("main:homepage")   

    if request.method == "POST":        
        if 'add-single-url-form' in request.POST:
            product_id = request.POST['product-name']
            new_url = request.POST['product-url']
            validator = URLValidator()
            try:
                validator(new_url)
            except ValidationError:
                return HttpResponse('oj nie kolego, to nie jest prawidlowy url')
            
            
            product = Product.objects.get(id=product_id)
            if not ProductUrls.objects.filter(product=product):
                new_obj = ProductUrls(product=product)
                new_obj.save()
            
            if request.user == product.user:
                db_urls = json.loads(ProductUrls.objects.get(product=product).urls)['urls']
                if new_url not in db_urls:
                    parsed_url = urlparse(new_url)
                    domain = parsed_url.netloc
                    
                    # TODO: validate more accurately url
                    store = None
                    try:
                        store = Store.objects.get(url=f"https://{domain}/")
                    except ObjectDoesNotExist:
                        try:
                            store = Store.objects.get(url=f"https://www.{domain}/")
                        except ObjectDoesNotExist:
                            return HttpResponse("Ten sklep nie jest obsługiwany. JEsli cos nie pasuje to napisz maila")
                        
                    if store:
                        db_urls.append([store.name, new_url])
                        json_urls = json.dumps({"urls": db_urls})
                        urls_model_obj = ProductUrls.objects.get(product=product)
                        urls_model_obj.urls = json_urls
                        print(urls_model_obj.urls)
                        urls_model_obj.save()
                    

    short_names = {
        'telegram': '<i title="Telegram" class="fa-brands fa-telegram"></i>',
        'email': '<i title="E-mail" class="fa-solid fa-at">',
        'sms': '<i title="SMS" class="fa-solid fa-comment-sms"></i>',
        'call': '<i title="Połączenie telefoniczne" class="fa-solid fa-phone"></i>',
    }
                    
    products = [
        {
            "product_name": product.product_name,
            "category_name": product.category.category_name,
            "wanted_price": product.wanted_price,
            "wanted_price_tolerance": product.wanted_price_tolerance,
            "lowest_price_notification_time_value": product.lowest_price_notification_time_value,
            "lowest_price_notification_time_unit": product.lowest_price_notification_time_unit,
            "lowest_price_notification_choices": [short_names[choice] for choice in json.loads(product.lowest_price_notifications)['choices']],
            "wanted_price_notification_choices": [short_names[choice] for choice in json.loads(product.wanted_price_notifications)['choices']],
            "urls_count": len(json.loads(ProductUrls.objects.get(product=product).urls)['urls']),
            "id": product.id,
        } for product in Product.objects.filter(user=request.user)
    ]
    
    context = {
        "products": products
    }
    
    return render(request, 'account/products.html', context=context)


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user != product.user:
        return HttpResponse("to nie twoj produkt kolego")
    
    
    
    context = {
        'product_name': product.product_name,
    }
    
    return render(request, 'product/product.html', context=context)


def data_account(request):
    if not request.user.is_authenticated:
        return redirect("main:homepage")
    
    if not UserData.objects.filter(user=request.user):
        new_user = UserData(user=request.user)
        new_user.save()
    
    def generate_api_key():
        api_key = uuid.uuid4()
        if UserData.objects.filter(promobot_api_key=api_key):
            generate_api_key()
        
        return api_key
    
    user_data = UserData.objects.get(user=request.user)
    
    if request.method == "POST":
        if 'generate-promobot-api-key' in request.POST and not user_data.promobot_api_key:
            new_api_key = generate_api_key()
            user_data.promobot_api_key = new_api_key
            user_data.save()
        if 'update-data' in request.POST:
            if request.POST['telegram_api_key']:
                user_data.telegram_api_key = request.POST['telegram_api_key']
            if request.POST['telegram_api_uid']:
                try:
                    new_uid = int(request.POST['telegram_api_uid'])
                    user_data.telegram_user_id = new_uid
                except ValueError:
                    # TODO: display error
                    print("nieprawidłowy telegram id")
                
            if request.POST['phone_number']:
                user_data.phone_number = '+48' + request.POST['phone_number']
            
            user_data.save()
            
    
    context = {
        'promobot_api_key': user_data.promobot_api_key,
        'telegram_api_key': user_data.telegram_api_key,
        'telegram_user_id': user_data.telegram_user_id,
        'phone_number': str(user_data.phone_number).replace("+48", "")
    }
    
    # print(context)
    
    return render(request, 'account/data.html', context)


def download(request):
    # download_obj = Download.objects.first()
    # urls = {
    #     "windows": download_obj.windows_version.url,
    #     "mac": download_obj.mac_version.url,
    #     "linux": download_obj.linux_version.url,
    # }
    
    # context = {
    #     "urls": urls,
    # }
    
    return render(request, "app/download.html")


def premium(request):
    return render(request, 'account/premium.html')


def premium_settings(request):
    return render(request, 'account/premium_settings.html')


def delete_account(request):
    if not request.user.is_authenticated:
        return redirect("main:homepage")
    return render(request, 'account/delete_account.html')


def available_stores(request):
    stores = Store.objects.all()
    print(stores)
    context = {
        "stores": stores,
    }
    return render(request, 'app/available_stores.html', context=context)


def about_page(request):
    return render(request, 'app/about.html')


def contact_page(request):
    return render(request, 'app/contact.html')


def report_bug_page(request):
    return render(request, 'app/report_bug.html')
