from .models import Product, UserProductInteraction
from django.db.models import Count
from django.core.cache import cache
from django.conf import settings

def recommend_products(user):
    cache_key = f"recommended_products_{user.id}"
    recommended_products = cache.get(cache_key)

    if not recommended_products:
        if user.is_authenticated:
            interactions = UserProductInteraction.objects.filter(user=user)
            if interactions.exists():
                product_ids = interactions.values_list('product_id', flat=True)
                recommended_products = Product.objects.filter(id__in=product_ids).distinct()
            else:
                recommended_products = Product.objects.annotate(
                    interactions_count=Count('userproductinteraction')
                ).order_by('-interactions_count')[:10]
        else:
            recommended_products = Product.objects.annotate(
                interactions_count=Count('userproductinteraction')
            ).order_by('-interactions_count')[:10]

        # Cache the result for a specific period
        cache.set(cache_key, recommended_products, timeout=settings.CACHE_TIMEOUT)

    return recommended_products