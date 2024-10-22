from django.contrib import admin
from .models import Doctors, DoctorCategory

admin.site.register(Doctors)
admin.site.register(DoctorCategory)