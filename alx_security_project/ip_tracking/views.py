from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit

@csrf_exempt
@ratelimit(key='ip', rate='5/m', block=True, method='POST')  # anonymous users
def anonymous_login_view(request):
    """
    Anonymous login rate limited: 5 request per minute per IP
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)

        if user:
            login(request,user)
            return JsonResponse({'message':'Login successfull'})
        else:
            return JsonResponse({'error':'Invalid credentials'},status=401)
        
    return JsonResponse({'error':'POST required'},status= 405)

@csrf_exempt
@ratelimit(key='ip',rate='10/m',block=True,method='POST') #auntheticated users
def user_sensitive_action(request):
    """
    Authenticated-only endpoint, limited to 10 request per minute per IP
    """

    if not request.user.is_authenticated:
        return JsonResponse({'error':'Authentication required'},status=403)
    
    # Example protection action
    return JsonResponse({'message':'Sensitive data accessed successfully'})