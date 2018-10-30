from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(HospitalArea)
admin.site.register(SectionInfo)
admin.site.register(DoctorInfo)
admin.site.register(DoctorSection)

