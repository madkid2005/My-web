from .models import Cart
from django.db.models import Sum

def cart_items_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.aggregate(Sum('quantity'))['quantity__sum'] or 0
    else:
        cart_items_count = 0
    
    return {'cart_items_count': cart_items_count}
