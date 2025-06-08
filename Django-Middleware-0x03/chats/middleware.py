# chats/middleware.py
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        with open('requests.log', 'a') as f:
            f.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Access allowed only between 6PM and 9PM.")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = {}

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        now = time.time()
        self.request_log.setdefault(ip, []).append(now)
        # Keep only messages from the last 60 seconds
        self.request_log[ip] = [t for t in self.request_log[ip] if now - t < 60]
        if request.method == 'POST' and len(self.request_log[ip]) > 5:
            return HttpResponseForbidden("Too many messages sent.")
        return self.get_response(request)

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            role = getattr(request.user, 'role', 'user')
            if role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Insufficient role permissions.")
        return self.get_response(request)
