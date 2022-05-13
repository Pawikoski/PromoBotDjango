from django.shortcuts import render, redirect
from .forms import NewUserForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


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
    return render(request, 'app/account.html')


def add_products(request):
    if not request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == "POST":
        print(request.POST)
        if 'form-name' not in request.POST.keys():
            return render(request, "app/add_products.html", {"errors": "Wystąpił niespodziewany błąd"})
        
        match request.POST['form-name']:
            case 'add-product':
                # TODO: handle product adding
                pass
        
        
    return render(request, 'app/add_products.html')
    


def available_stores(request):
    return render(request, 'app/available_stores.html')


def about_page(request):
    return render(request, 'app/about.html')


def contact_page(request):
    return render(request, 'app/contact.html')


def report_bug_page(request):
    return render(request, 'app/report_bug.html')
