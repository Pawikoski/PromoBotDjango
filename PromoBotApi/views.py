from django.http import JsonResponse

# Create your views here.
def verify(request):
    print(request.POST)
    


def main(request):
    return JsonResponse({"error": "Please provide an endpoint"})
