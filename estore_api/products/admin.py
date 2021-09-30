from django.contrib import admin

from estore_api.products import models

admin.site.register(models.Image)
admin.site.register(models.Category)
admin.site.register(models.Series)
admin.site.register(models.Unit)
admin.site.register(models.Color)
admin.site.register(models.Brand)
admin.site.register(models.OS)
admin.site.register(models.CPU)
admin.site.register(models.GPU)
admin.site.register(models.Storage)
admin.site.register(models.DisplayType)
admin.site.register(models.DisplayResolution)
admin.site.register(models.Display)
admin.site.register(models.Notebook)
admin.site.register(models.Phone)
