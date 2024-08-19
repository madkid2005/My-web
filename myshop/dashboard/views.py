from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import SellerProfile
from products.models import Product
from orders.models import Order
from accounts.forms import SellerBankDetailsForm
from products.forms import ProductReviewForm, ProductForm

@login_required
def seller_dashboard(request):
    seller_profile = request.user.seller_profile
    products = Product.objects.filter(seller=seller_profile)
    orders = Order.objects.filter(items__product__seller=seller_profile).distinct()
    
    # Summarize data for overview
    total_sales = orders.filter(status='completed').count()
    total_revenue = sum(order.total_price for order in orders.filter(status='completed'))
    
    context = {
        'seller_profile': seller_profile,
        'products': products,
        'orders': orders,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def manage_products(request):
    products = Product.objects.filter(seller=request.user.seller_profile)
    return render(request, 'dashboard/manage_products.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller_profile
            product.save()
            return redirect('manage_products')
    else:
        form = ProductForm()
    return render(request, 'dashboard/add_product.html', {'form': form})

@login_required
def edit_product(request, product_id):
    # Get the product to edit, ensuring it belongs to the current seller
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller_profile)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  # Save the updated product
            return redirect('manage_products')  # Redirect to the product management page
    else:
        form = ProductForm(instance=product)  # Populate the form with the product's existing data

    return render(request, 'dashboard/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller_profile)
    if request.method == 'POST':
        product.delete()
        return redirect('manage_products')
    return render(request, 'dashboard/delete_product.html', {'product': product})

@login_required
def view_orders(request):
    orders = Order.objects.filter(items__product__seller=request.user.seller_profile).distinct()
    return render(request, 'dashboard/view_orders.html', {'orders': orders})

@login_required
def update_bank_details(request):
    seller_profile = request.user.seller_profile
    if request.method == 'POST':
        form = SellerBankDetailsForm(request.POST, instance=seller_profile)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = SellerBankDetailsForm(instance=seller_profile)
    return render(request, 'dashboard/update_bank_details.html', {'form': form})



