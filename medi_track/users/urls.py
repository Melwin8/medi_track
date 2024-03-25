"""
URL configuration for medi_track project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('hospital-register/',views.HospitalRegistrationView.as_view()),
    path('doctor-register/', views.DoctorRegistrationView.as_view()),
    path('patient-register/', views.PatientRegistrationView.as_view()),
    path('login/', views.UserloginView.as_view()),

    path('add-departments/', views.DepartmentCreateAPIView.as_view()),
    path('list-departments-of-authenticated-hospital/', views.DepartmentListofAuthenticatedHospitalAPIView.as_view()),
    path('list-doctors-of-authenticated-hospital/', views.DoctorListofAuthenticatedHospitalAPIView.as_view()),
    path('doctor-detail/<int:doctor_id>/', views.DoctorDetailAPIView.as_view(),),
]
