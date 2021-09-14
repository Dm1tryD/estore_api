from django.contrib import admin

from estore_api.products.models import Notebook, Phone

admin.site.register(Notebook)
admin.site.register(Phone)
