# api/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, PatientSerializer, DoctorSerializer, PatientDoctorMappingSerializer, DoctorMappingSerializer
from .models import Patient, Doctor, PatientDoctorMapping

# HTML Views
def login(request):
    return render(request, 'login.html') 

def function(request):
    return render(request, 'function.html')

def mappings_page(request):
    return render(request, 'mapping.html')

def register(request):
    return render(request, 'register.html')

# API Views
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
        
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Allow all users to see all doctors, regardless of who created them
        return Doctor.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]
    
class PatientDoctorsView(generics.ListAPIView):
    serializer_class = DoctorMappingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return PatientDoctorMapping.objects.filter(patient_id=patient_id)