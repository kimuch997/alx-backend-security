from django.core.cache import cache
from django.http import HttpResponseForbidden
from .models import RequestLog,BlockedIP
from django.utils.timezone import now
import requests

class IPLoggingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        # Get the client IP
        ip_address = request.META.get('REMOTE_ADDR')

        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access denied: your IP has been blocked.")

        cached_data = cache.get(ip_address)
        if cached_data:
            country,city = cached_data
        else:
            # Step 3:Fetch geolocation via external API()
            try:
                response = requests.get(f"https//ipinfo.io/{ip_address}/json")
                data = response.json
                country = data.get("city","")
                # cache for 24 hrs
                cache.set(ip_address,(country,city),timeout=60*60*24)
            except Exception:
                country,city="", ""

        # Log details
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=request.path
        )
    # Continue processing the request
        response = self.get_response(request)
        return response