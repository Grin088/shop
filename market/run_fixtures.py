import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.core.management import call_command

files = os.listdir('fixtures')
for i in files:
    call_command('loaddata', 'fixtures/' + i)
