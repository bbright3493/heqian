from django.contrib import admin
from .models import *

# Register your models here.

admin.site.site_header = '禾乾医疗后台数据管理系统' # 设置标题
admin.site.site_title = '禾乾医疗后台数据管理系统' # 设置标题

admin.site.register(HospitalArea)
admin.site.register(SectionInfo)
admin.site.register(DoctorInfo)
admin.site.register(DoctorSection)
admin.site.register(Schedule)
admin.site.register(HosptialIntroduce)
admin.site.register(HosptialCulture)
admin.site.register(HosptialBanner)
admin.site.register(HosptialKnow)
admin.site.register(HosptialProject)
admin.site.register(CultureBanner)
