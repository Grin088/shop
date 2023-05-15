from django.contrib import admin
from mptt.admin import MPTTModelAdmin


from catalog.models import MPTTCatalog

admin.site.register(MPTTCatalog, MPTTModelAdmin)
