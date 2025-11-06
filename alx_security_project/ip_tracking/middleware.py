from .models import RequestLog
from django.utils.timezone import now

class IPLoggingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        # Get the client IP
        ip_address = request.META.get('REMOTE_ADDR')

        # Log details
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=request.path
        )
    # Continue processing the request
        response = self.get_response(request)
        return response