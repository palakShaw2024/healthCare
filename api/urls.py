# api/urls.py
from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import (
    RegisterView, PatientViewSet, DoctorViewSet, 
    PatientDoctorMappingViewSet, PatientDoctorsView
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'mappings', PatientDoctorMappingViewSet, basename='mapping')

urlpatterns = [
    # HTML Page URLs
    path('login/', views.login, name='login-page'),
    path('register/', views.register, name='register-page'),
    path('function/', views.function, name='function-page'),
    path('mapping/', views.mappings_page, name='mapping-page'),
    
    # REST API Endpoints
    path('api/auth/register/', RegisterView.as_view(), name='api-register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='api-login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('api/', include(router.urls)),
    path('api/mappings/<int:patient_id>/', PatientDoctorsView.as_view(), name='patient-doctors'),

    path('admin/', admin.site.urls),
]