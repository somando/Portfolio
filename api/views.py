from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def top(request):
    
    if request.method == 'GET':
        
        return JsonResponse({'status': 'Success', 'message': 'Hello, API!'})
    
    elif request.method == 'POST':
        
        if 'message' not in request.POST:
            
            return JsonResponse({'status': 'Failure', 'message': 'Message is required.'})
        
        message = request.POST['message']
        
        return JsonResponse({'status': 'Success', 'message': message})
