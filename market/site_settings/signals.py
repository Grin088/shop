from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
# from django.urls import reverse
# from site_settings.models import SiteSettings


@receiver(post_save, sender=None)
def clear_home_cache(*args, **kwargs):
    cache.delete('home')
