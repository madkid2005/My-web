from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseForbidden

# Custom Admin Access Restriction Middleware
def admin_only(request):
    if request.user.is_superuser and request.user.username == "kiarash":  
        return None  # Allow access
    return HttpResponseForbidden("Access denied.")  # Deny access to others


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard', include('dashboard.urls')),
    path('order', include('orders.urls')),
    path('products', include('products.urls')),
    path('cart', include('cart.urls')),



]

admin.site.login = admin_only

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)