from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(CustomUser)
admin.site.register(Hospital)
admin.site.register(Department)