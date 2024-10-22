from rest_framework import serializers
from .models import DoctorCategory, Doctors
from django.utils import timezone
from datetime import timedelta


class DoctorsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorCategory
        fields = ['id','name','imageUrl']
        
class GetAllDocsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Doctors
        fields = ['id','name', 'category', 'rating', 'time_slot','picture','experience','appointment_fee','location','city', 'cities','clinic_name', 'mapLink','phone']