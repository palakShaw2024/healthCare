

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    
    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    
    def __str__(self):
        return self.name

class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('patient', 'doctor')
        
    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name}"
