from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from products.models import Product
from .models import Order, OrderItem, Payment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from decimal import Decimal
from cart.models import Cart
from django.views.decorators.csrf import csrf_exempt
import zarinpal


@login_required
@transaction.atomic
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = cart.get_total_price()
    
    if cart.items.count() == 0:
        return redirect('cart_detail')

    if request.method == 'POST':
        # Create an order
        order = Order.objects.create(
            buyer=request.user,
            total_price=total_price,
            shipping_address=request.POST.get('shipping_address'),
        )
        
        # Add order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.display_price
            )
        
        # Clear the cart
        cart.items.all().delete()
        
        # Redirect to payment view
        return redirect('payment_view', order_id=order.id)

    return render(request, 'orders/checkout.html', {'total_price': total_price})

@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    if request.method == 'POST':
        zarinpal_merchant_id = settings.ZARINPAL_MERCHANT_ID
        site_fee = order.total_price * Decimal('0.06')
        seller_amount = order.total_price - site_fee

        # Initialize ZarinPal client without the sandbox argument
        zarinpal_client = zarinpal.ZarinPal(merchant_id=zarinpal_merchant_id)
        
        # Prepare the payment request
        description = f'Payment for Order {order_id}'
        callback_url = request.build_absolute_uri(reverse('payment_callback', args=[order.id]))
        result = zarinpal_client.payment_request(
            amount=int(order.total_price),  # amount in toman
            description=description,
            mobile=request.user.phone_number,
            callback_url=callback_url,
        )

        if result['Status'] == 100:
            return redirect(result['url'])
        else:
            return JsonResponse({'error': 'Payment request failed'}, status=400)
    
    return render(request, 'payment.html', {'order': order})

def payment_callback(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    authority = request.GET.get('Authority')
    zarinpal_client = zarinpal.ZarinPal(merchant_id=settings.ZARINPAL_MERCHANT_ID, sandbox=settings.ZARINPAL_SANDBOX)
    
    result = zarinpal_client.payment_verification(
        authority=authority,
        amount=int(order.total_price)
    )

    if result['Status'] == 100:
        site_fee = order.total_price * Decimal('0.06')
        seller_amount = order.total_price - site_fee

        # Distribute payment
        distribute_payment(order, seller_amount, site_fee)

        order.payment_status = 'paid'
        order.status = 'confirmed'
        order.save()

        return JsonResponse({'status': 'Payment successful', 'RefID': result['RefID']})
    else:
        return JsonResponse({'error': 'Payment verification failed'}, status=400)

def distribute_payment(order, seller_amount, site_fee):
    seller = order.items.first().product.seller.user.seller_profile

    # Log or print for testing
    print(f"Transferring {seller_amount} toman to seller account: {seller.bank_account_number}")
    print(f"Transferring {site_fee} toman to site owner's account")

    seller.number_of_sales += 1
    seller.save()




























# from django.shortcuts import render, get_object_or_404, redirect
# from django.urls import reverse
# from django.conf import settings
# from products.models import Product
# from .models import Order, OrderItem, Payment
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.db import transaction
# from decimal import Decimal
# from django.views.decorators.csrf import csrf_exempt
# import zarinpal

# @login_required
# @transaction.atomic
# def create_order(request):
#     buyer = request.user
#     cart = request.session.get('cart', {})  # Assuming cart is stored in session

#     if not cart:
#         return JsonResponse({'error': 'Cart is empty'}, status=400)

#     order = Order.objects.create(buyer=buyer, shipping_address=buyer.address, total_price=0)
#     total_price = 0

#     for product_id, quantity in cart.items():
#         product = get_object_or_404(Product, id=product_id)
#         if product.stock < quantity:
#             return JsonResponse({'error': f'Not enough stock for {product.name}'}, status=400)
#         order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
#         product.stock -= quantity
#         product.save()
#         total_price += order_item.get_total_item_price()

#     order.total_price = total_price
#     order.save()

#     # Clear the cart
#     request.session['cart'] = {}

#     return redirect('payment', order_id=order.id)

# def payment_view(request, order_id):
#     order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
#     if request.method == 'POST':
#         zarinpal_merchant_id = settings.ZARINPAL_MERCHANT_ID
#         site_fee = order.total_price * Decimal('0.06')
#         seller_amount = order.total_price - site_fee

#         zarinpal_client = zarinpal.ZarinPal(merchant_id=zarinpal_merchant_id, sandbox=settings.ZARINPAL_SANDBOX)
        
#         # Prepare the payment request
#         description = f'Payment for Order {order_id}'
#         callback_url = request.build_absolute_uri(reverse('payment_callback', args=[order.id]))
#         result = zarinpal_client.payment_request(
#             amount=int(order.total_price),  # amount in toman
#             description=description,
#             mobile=request.user.phone_number,
#             callback_url=callback_url,
#         )

#         if result['Status'] == 100:
#             return redirect(result['url'])
#         else:
#             return JsonResponse({'error': 'Payment request failed'}, status=400)
    
#     return render(request, 'payment.html', {'order': order})

# def payment_callback(request, order_id):
#     order = get_object_or_404(Order, id=order_id, buyer=request.user)
#     authority = request.GET.get('Authority')
#     zarinpal_client = zarinpal.ZarinPal(merchant_id=settings.ZARINPAL_MERCHANT_ID, sandbox=settings.ZARINPAL_SANDBOX)
    
#     result = zarinpal_client.payment_verification(
#         authority=authority,
#         amount=int(order.total_price)
#     )

#     if result['Status'] == 100:
#         # Payment was successful, distribute the funds
#         site_fee = order.total_price * Decimal('0.06')
#         seller_amount = order.total_price - site_fee

#         # Assume distribute_payment handles the actual fund transfer logic
#         distribute_payment(order, seller_amount, site_fee)

#         order.payment_status = 'paid'
#         order.status = 'confirmed'
#         order.save()

#         return JsonResponse({'status': 'Payment successful', 'RefID': result['RefID']})
#     else:
#         return JsonResponse({'error': 'Payment verification failed'}, status=400)

# def distribute_payment(order, seller_amount, site_fee):
#     seller = order.items.first().product.seller.user.seller_profile

#     # Log or print for testing
#     print(f"Transferring {seller_amount} toman to seller account: {seller.bank_account_number}")
#     print(f"Transferring {site_fee} toman to site owner's account")

#     # Implement the logic to transfer funds to the seller's bank account
#     # For simplicity, this might involve directly calling the payment gateway's API
#     # to perform the transfer, or it could be done manually for small platforms.

#     seller.number_of_sales += 1
#     seller.save()

# @login_required
# def order_status_view(request, order_id):
#     order = get_object_or_404(Order, id=order_id, buyer=request.user)
#     return JsonResponse({'order_id': order.id, 'status': order.status, 'payment_status': order.payment_status})

# @login_required
# def seller_orders_view(request):
#     if not request.user.is_seller:
#         return JsonResponse({'error': 'Only sellers can view this page'}, status=403)
    
#     orders = Order.objects.filter(items__product__seller=request.user.seller_profile).distinct()
#     order_data = [{
#         'order_id': order.id,
#         'buyer': order.buyer.username,
#         'total_price': order.total_price,
#         'status': order.status
#     } for order in orders]
    
#     return JsonResponse({'orders': order_data})
