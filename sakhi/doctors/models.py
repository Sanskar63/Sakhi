import json
from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group, Permission, AbstractBaseUser, BaseUserManager


class DoctorCategory(models.Model):
    name = models.CharField(max_length=50) 
    imageUrl=models.CharField(max_length=10000,default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkoyUQaux4PEUmEPGc7PodeN8XbgC4aOBsug&s")
    doctors = models.ManyToManyField('Doctors', related_name='categories')

    def __str__(self):
        return self.name


class Doctors(models.Model):
    # Clinic details
    name=models.CharField(max_length=50)
    phone = models.CharField(max_length=10,unique=True, blank=True, null=True, validators=[RegexValidator(regex=r"^\d{10}", message="Phone number must be 10 digits only.")])
    email=models.EmailField(null=True,blank=True,unique=True)
    gender=models.CharField(max_length=10,blank=True,null=True)
    dob = models.DateField(null=True, blank=True)
    location=models.CharField(max_length=100,blank=True,null=True)
    REQUIRED_FIELDS=["name"]
    USERNAME_FIELD='phone'
    
    clinic_name = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)

    # Store cities as a JSON-encoded string in TextField
    cities = models.TextField(
        blank=False,
        default='[]',
        help_text="Please fill this field, or your profile will not be shown to users."
    )
    
    mapLink = models.CharField(max_length=200, blank=True, null=True)

    # Professional details
    specialization = models.CharField(max_length=255, blank=True, null=True)
    appointment_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(DoctorCategory, related_name="doctor_category", on_delete=models.CASCADE, null=True, blank=True)

    # Personal and document details
    picture = models.CharField(max_length=10000, blank=True, null=True)
    qualification = models.CharField(max_length=100, default="MBBS", null=True, blank=True)
    qualification_doc = models.CharField(max_length=10000, blank=True, null=True)
    identity_doc = models.CharField(max_length=10000, blank=True, null=True)
    degree_filename = models.CharField(max_length=10000, blank=True, null=True)

    # Experience and bio
    experience = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)])  # Overall experience
    bio = models.CharField(max_length=10000, null=True, blank=True)

    # Pricing and ratings
    rating = models.IntegerField(default=0)
    rating_no = models.IntegerField(default=0)

    # Time slots stored as a JSON-encoded string
    time_slot = models.TextField(blank=True, null=True, default='[]')

    def __str__(self):
        return f"{self.id} - {self.name}"

    def save(self, *args, **kwargs):
        # Ensure all cities are in lowercase before saving
        self.cities = json.dumps([city.lower() for city in json.loads(self.cities)])
        super().save(*args, **kwargs)

    def get_cities(self):
        """Return cities as a list."""
        return json.loads(self.cities)

    def set_cities(self, cities_list):
        """Set cities from a list."""
        self.cities = json.dumps(cities_list)

    def get_time_slot(self):
        """Return time_slot as a list."""
        return json.loads(self.time_slot)

    def set_time_slot(self, time_slot_list):
        """Set time_slot from a list."""
        self.time_slot = json.dumps(time_slot_list)