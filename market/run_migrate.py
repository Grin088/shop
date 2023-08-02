import os
import django
from django.core.management import call_command


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

list_app = ['cart', 'catalog', 'discounts', 'products', 'shops', 'users']

for comm in list_app:
    call_command("makemigrations", comm)
call_command("migrate")
