from django.http import JsonResponse

# Create your views here.

def api_home(requests):
    return JsonResponse({"test":"hi"})
