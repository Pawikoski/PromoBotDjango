from django.shortcuts import render, redirect
from .forms import NewUserForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Category, ProductUrls


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
            return redirect("homepage")
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
                return redirect("homepage")
            else:
                messages.error(request, "Nieprawidłowa nazwa użytkownika lub hasło")
        else:
            messages.error(request, "Nieprawidłowa nazwa użytkownika lub hasło")

    form = AuthenticationForm()
    return render(request, "app/login.html", {"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Zostałeś wylogowany")
    return redirect('homepage')


def user_page(request):
    if not request.user.is_authenticated:
        return redirect("homepage")
    
    if request.method == "POST":
        if 'form-name' not in request.POST.keys():
            return render(request, "app/add_products.html", {"errors": "Wystąpił niespodziewany błąd"})
       
        if request.POST['form-name'] == 'add-category':
            category_name = request.POST['category-name']
            if Category.objects.filter(category=category_name, user=request.user):
                return render(request, 'app/account.html', {"errors": "Kategoria o wybranej nazwie już istnieje"})
            
            new_category = Category(category=category_name, user=request.user)
            new_category.save()
        
    return render(request, 'app/account.html')


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
        
        if request.POST['form-name'] == 'add-product':
            category = data['category']
            product_name = data['product-name']
            
            try:
                wanted_price = int(data['wanted-price'])
                wanted_price_tolerancy = int(data['wanted-price-tolerancy'])
                
                if wanted_price < 1 or wanted_price_tolerancy < 0 or wanted_price_tolerancy > 20:
                    raise ValueError
            except ValueError:
                return render(request, 'app/add_products.html', context = {"available_categories": categories, "errors": ["Błąd. Sprawdź dane i spróbuj ponownie"]})
            
            main_notification_choices = data.getlist('main-notify')
                
                
        
    return render(request, 'app/add_products.html', context=context)
    


def available_stores(request):
    return render(request, 'app/available_stores.html')


def about_page(request):
    return render(request, 'app/about.html')


def contact_page(request):
    return render(request, 'app/contact.html')


def report_bug_page(request):
    return render(request, 'app/report_bug.html')
