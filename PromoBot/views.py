from django.shortcuts import redirect, render, HttpResponse
from ipware import get_client_ip

# Create your views here.

def verify_ip(view):
    def wrapper(request):
        if 1 == 2:
            return redirect('main:homepage')
        
        return view(request)
        
    return wrapper
    

@verify_ip
def index(request):
    print(request.META['REMOTE_ADDR'])
    return HttpResponse("sadfasd")