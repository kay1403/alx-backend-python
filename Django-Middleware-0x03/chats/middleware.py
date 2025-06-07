# chats/middleware.py
from datetime import datetime
import logging
import os

# Configure logger (ensure log directory exists)
log_dir = os.path.join(os.path.dirname(__file__), '..', 'requests.log')
logging.basicConfig(filename=log_dir, level=logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_entry)
        return self.get_response(request)
