from django.http import HttpResponseForbidden
from .models import RequestLog,BlockedIP
from django.utils.timezone import now

class IPLoggingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        # Get the client IP
        ip_address = request.META.get('REMOTE_ADDR')

        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access denied: your IP has been blocked.")

        # Log details
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=request.path
        )
    # Continue processing the request
        response = self.get_response(request)
        return response