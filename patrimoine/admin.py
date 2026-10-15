from django.contrib import admin
from .models import *
for model in [Site,Organisation,Room,Equipment,ITAsset,Vehicle,Maintenance,AuditLog]: admin.site.register(model)
