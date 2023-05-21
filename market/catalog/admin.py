from django.contrib import admin
from mptt.admin import MPTTModelAdmin


from catalog.models import Catalog

admin.site.register(Catalog, MPTTModelAdmin)
