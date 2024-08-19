from django.http import HttpResponseForbidden

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and request.user.is_authenticated:
            if not (request.user.is_superuser and request.user.username == "kiarash"):  # Replace with your username
                return HttpResponseForbidden("Access denied.")
        return self.get_response(request)
