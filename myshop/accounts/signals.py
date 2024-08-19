from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import BuyerProfile, SellerProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_buyer:
            BuyerProfile.objects.create(user=instance)
        if instance.is_seller:
            SellerProfile.objects.create(user=instance)
