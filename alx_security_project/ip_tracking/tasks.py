from celery import shared_task
from django.utils.timezone import now, timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies():
    """
    Detect IPs making over 100 requests/hour
    or accessing sensitive paths (/admin, /login).
    """
    one_hour_ago = now() - timedelta(hours=1)
    recent_requests = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    # Count requests per IP
    ip_counts = {}
    for req in recent_requests:
        ip_counts[req.ip_address] = ip_counts.get(req.ip_address, 0) + 1

        # Check sensitive paths
        if '/admin' in req.path or '/login' in req.path:
            SuspiciousIP.objects.get_or_create(
                ip_address=req.ip_address,
                reason='Accessed sensitive path'
            )

    # Flag IPs exceeding 100 requests/hour
    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                reason=f'Exceeded {count} requests in 1 hour'
            )
