from django.db import models
from django.contrib.auth.models import User
import uuid

# Your existing Feature model
class Feature(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

# New models for the booking system
class Service(models.Model):
    SERVICE_CHOICES = [
        ('solar', 'Solar Panel Consultation'),
        ('ev', 'EV Charging Consultation'),
        ('smart', 'Smart Home Energy Management Consultation'),
    ]
    
    name = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    description = models.TextField()
    
    def __str__(self):
        return dict(self.SERVICE_CHOICES).get(self.name)

class Booking(models.Model):
    PROPERTY_CHOICES = [
        ('detached', 'Detached House'),
        ('semi-detached', 'Semi-Detached House'),
        ('terraced', 'Terraced House'),
        ('flat', 'Flat/Apartment'),
        ('bungalow', 'Bungalow'),
        ('commercial', 'Commercial Property'),
    ]
    
    # Link to user if authenticated
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Personal details
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    property_type = models.CharField(max_length=50, choices=PROPERTY_CHOICES)
    notes = models.TextField(blank=True, null=True)
    
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    booking_reference = models.CharField(max_length=20, unique=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.full_name} - {self.booking_reference}"
    
    def save(self, *args, **kwargs):
        # Generate booking reference if not already set
        if not self.booking_reference:
            self.booking_reference = f"BOL-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

class TimeSlot(models.Model):
    date = models.DateField()
    time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('date', 'time')
    
    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} {self.time.strftime('%H:%M')}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.subject} - {self.name}"