from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Shipping

@receiver(post_save, sender=Order)
def create_shipping(sender, instance, created, **kwargs):
    if created and instance.status == 'confirmed':
        Shipping.objects.create(order=instance)
