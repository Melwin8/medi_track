from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from users.permissions import IsHospitalUser, IsDoctorUser, IsPatientUser
from patient.models import (Appointment)
from patient.serializers import (AppointmentSerializer)
from .models import *
from .serializers import *
from django.http import JsonResponse

class DoctorAppointmentsListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDoctorUser]
    def get(self, request):
        try:
            doctor = request.user.doctor
            appointments = Appointment.objects.filter(doctor=doctor)
            serializer = AppointmentSerializer(appointments, many=True)
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from datetime import datetime
class Get_time_choices(APIView):
    def get(self, request):
        print(timezone.now().strftime('%H:%M:%S'))
        print(datetime.now().time())
        print(timezone.now())
        print(datetime.now())
        time_choices= PrescriptionMedicine.time_choices
        return JsonResponse(dict(time_choices), safe=False)

class PrescriptionCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDoctorUser]
    serializer_class=PrescriptionSerializer

    def post(self, request,appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            print(appointment.id)
            doctor = appointment.doctor
            hospital = appointment.hospital
            patient = appointment.user
            data = {
                'patient': patient,
                'doctor': doctor,
                'appointment': appointment,
                'hospital': hospital,
            }


            serializer = PrescriptionSerializer(data=request.data)

            if serializer.is_valid():

                serializer.save(**data)

                return Response({"status":1,"data":serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DoctorPrescriptionsListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDoctorUser]
    def get(self, request):
        try:
            doctor = request.user.doctor
            prescription = Prescription.objects.filter(doctor=doctor)
            serializer = DetailedPrescriptionSerializer(prescription, many=True)
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PrescriptionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, prescription_id, *args, **kwargs):
        try:

            prescription = Prescription.objects.get(pk=prescription_id)

            serializer = DetailedPrescriptionSerializer(prescription)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Prescription.DoesNotExist:

            return Response(" not found.", status=status.HTTP_404_NOT_FOUND)
        

from .tasks import *
from django.shortcuts import render    
from django.http import HttpResponse   
def test(request):
    send_notification_based_on_times.delay()
    return HttpResponse("doneeee")

            # return Response(" not found.", status=status.HTTP_404_NOT_FOUND)

