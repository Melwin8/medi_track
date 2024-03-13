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
from .views import *

urlpatterns = [
    path('Hospital-list/', HospitalListAPIView.as_view()),
    path('Doctors-list-by-hospital/<int:hospital_id>/', DoctorListofHospitalAPIView.as_view()),

    path('search-hospital/', SearchHospitalAPIView.as_view(),),
    path('search-doctors/', SearchDoctorsAPIView.as_view(),),



    path('book-appointment/', BookAppointmentAPIView.as_view()),
    path('available-slots/<int:doctor_id>/<str:day>/', AvailableSlotsAPIView.as_view(),),
    path('list-patient-appointments/', ListPatientAppointmentsAPIView.as_view(),),
    path('cancel-appointment/<int:appointment_id>/', CancelAppointmentAPIView.as_view(),),

    path('list-patient-prescription/', PatientPrescriptionsListAPIView.as_view(),),
]
