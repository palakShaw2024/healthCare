# api/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctorMapping

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
    
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['name', 'email']
        read_only_fields = ['created_by']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ['created_by']

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = '__all__'
        
class DoctorMappingSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'doctor', 'doctor_name', 'specialization']