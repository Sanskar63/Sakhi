from django.urls import path
from .views import *

urlpatterns = [
    path('all/', GetDoctors.as_view(), name='GetDoctors'),
    path('categories/', GetCategories.as_view(), name='GetCategories'),
]