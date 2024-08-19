from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, UserProductInteraction
from django.contrib.auth.decorators import login_required
from .forms import ProductReviewForm
from .recommendations import recommend_products
from .forms import FavoriteCategoriesForm
from orders.models import Order

# showing by interest
def main_page(request):
    # Default to all products
    products = Product.objects.all()

    # Get recommended products if the user is logged in and has interaction data
    recommended_products = recommend_products(request.user)

    return render(request, 'products/main_page.html', {
        'products': products,
        'recommended_products': recommended_products,
    })
       
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(stock__gt=0)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'products/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    reviews = product.reviews.all()

    # Track product view interaction
    if request.user.is_authenticated:
        UserProductInteraction.objects.create(user=request.user, product=product, interaction_type='view')

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'reviews': reviews
    })

@login_required
def add_product_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the user has purchased this product
    if not Order.objects.filter(user=request.user, items__product=product).exists():
        return redirect('product_detail', product_id=product.id)  # Or show an error message

    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductReviewForm()

    return render(request, 'products/add_product_review.html', {'form': form, 'product': product})

# update interests
@login_required
def update_preferences(request):
    if request.method == 'POST':
        form = FavoriteCategoriesForm(request.POST, instance=request.user.buyer_profile)
        if form.is_valid():
            form.save()
            return redirect('main_page')
    else:
        form = FavoriteCategoriesForm(instance=request.user.buyer_profile)

    return render(request, 'update_preferences.html', {'form': form})


# interested products
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Track product view interaction
    if request.user.is_authenticated:
        UserProductInteraction.objects.create(user=request.user, product=product, interaction_type='view')

    return render(request, 'products/product_detail.html', {'product': product})