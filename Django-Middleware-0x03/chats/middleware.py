import logging
import os
import time
from datetime import datetime
from collections import defaultdict
from django.http import HttpResponseForbidden, JsonResponse

# === MIDDLEWARE 1: Logging User Requests ===

# Configure logger to write into requests.log
log_file_path = os.path.join(os.path.dirname(__file__), '..', 'requests.log')
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        path = request.path
        logging.info(f"User: {user} - Path: {path}")
        return self.get_response(request)


# === MIDDLEWARE 2: Restrict Access By Time ===

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        if now.hour < 18 or now.hour >= 21:  # Outside 6PM to 9PM
            return HttpResponseForbidden("Chat access is restricted to 6PM - 9PM only.")
        return self.get_response(request)


# === MIDDLEWARE 3: Offensive Language / Rate Limiting ===

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_messages = defaultdict(list)
        self.limit = 5  # max messages per window
        self.window_seconds = 60  # 1 minute window

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/chat/"):
            ip = request.META.get('REMOTE_ADDR')
            now = time.time()
            # Keep only recent timestamps
            self.ip_messages[ip] = [t for t in self.ip_messages[ip] if now - t < self.window_seconds]
            if len(self.ip_messages[ip]) >= self.limit:
                return JsonResponse({"error": "Rate limit exceeded. Try again later."}, status=429)
            self.ip_messages[ip].append(now)
        return self.get_response(request)


# === MIDDLEWARE 4: Role Permission Check ===

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/chat/") and request.method in ["POST", "DELETE"]:
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            # Check role
            role = getattr(user, 'role', None)
            if role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to perform this action.")
        return self.get_response(request)
