from datetime import datetime
from django.http import HttpResponseForbidden
import time
import os
from django.conf import settings


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        print("[Middleware] RequestLoggingMiddleware loaded ✅")
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_dir = os.path.join(settings.BASE_DIR, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'requests.log')

        with open(log_file, 'a') as f:
            f.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        print("[Middleware] RestrictAccessByTimeMiddleware loaded ✅")
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Access allowed only between 6PM and 9PM.")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        print("[Middleware] OffensiveLanguageMiddleware loaded ✅")
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


class RolePermissionMiddleware:  # ✅ Corrigé ici (casse correcte)
    def __init__(self, get_response):
        print("[Middleware] RolePermissionMiddleware loaded ✅")
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            role = getattr(request.user, 'role', 'user')
            if role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Insufficient role permissions.")
        return self.get_response(request)
