from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages


# Create your views here.
def homepage(request):
    return render(request, 'app/homepage.html')


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Rejstracja przebiegła pomyślnie.")
            return redirect("homepage")
        messages.error(request, "Podczas rejestracji wystąpił błąd. Nieprawidłowe informacje")

    form = NewUserForm()
    return render(request, 'app/register.html', {"register_form": form})


def login(request):
    return render(request, 'app/login.html')
