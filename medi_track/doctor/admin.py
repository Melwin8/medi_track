from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(PrescriptionMedicine)

admin.site.register(Prescription)
admin.site.register(Notification)

# admin.site.register(Prescription)

