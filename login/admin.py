from django.contrib import admin
from login import models

# Register your models here.

admin.site.register(models.trans_data)
admin.site.register(models.balance_data)
admin.site.register(models.key_pair1)
admin.site.register(models.notification)


