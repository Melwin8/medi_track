from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from users.permissions import IsHospitalUser, IsDoctorUser, IsPatientUser
from users.models import (Hospital,CustomUser,Department,Doctor,Patient)
from doctor.models import (Prescription)
from doctor.serializers import (PrescriptionSerializer)
from .serializers import *
from .models import *


class HospitalListAPIView(APIView):
    permission_classes = [IsAuthenticated,IsPatientUser]
    def get(self, request, *args, **kwargs):
        try:

            hospitals = Hospital.objects.all().order_by('name')
            serializer = AllHospitalSerializer(hospitals, many=True)
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except Hospital.DoesNotExist:
            return Response("Hospitals does not exist.", status=status.HTTP_404_NOT_FOUND)


class DoctorListofHospitalAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, hospital_id, *args, **kwargs):
        try:
            doctors = Doctor.objects.filter(hospital=hospital_id)
            serializer = DoctorsSerializer(doctors,many=True)
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response("Doctors not found.", status=status.HTTP_404_NOT_FOUND)


class SearchHospitalAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('hospital_name')
        try:
            if search_query:
                hospitals = Hospital.objects.filter(name__icontains=search_query).order_by('name')
            else:
                return Response([], status=status.HTTP_200_OK)
            serializer = AllHospitalSerializer(hospitals, many=True)
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle any exceptions and return an error response
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchDoctorsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request, *args, **kwargs):
        doctor_query = request.query_params.get('doctor_name')
        hospital_query = request.query_params.get('hospital_name')
        try:
            if doctor_query and hospital_query:
                doctors = Doctor.objects.filter(name__icontains=doctor_query, hospital__name__icontains=hospital_query)
            elif doctor_query:
                doctors = Doctor.objects.filter(name__icontains=doctor_query)
            elif hospital_query:
                doctors = Doctor.objects.filter(hospital__name__icontains=hospital_query)
            else:
                return Response([], status=status.HTTP_200_OK)

            serializer = DoctorsSerializer(doctors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class BookAppointmentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPatientUser]
    def post(self, request, *args, **kwargs):
        try:
            serializer = AppointmentSerializer(data=request.data)
            if serializer.is_valid():
                # Check if the requested time slot is available
                doctor = serializer.validated_data['doctor']
                doctor_id = serializer.validated_data['doctor'].id
                day = serializer.validated_data['day']
                time = serializer.validated_data['time']
                if Appointment.objects.filter(doctor_id=doctor_id, day=day, time=time).exists():
                    return Response({"status": 0,"data":"This appointment slot is already booked."}, status=status.HTTP_400_BAD_REQUEST)

                # If the slot is available, save the appointment
                print(doctor)
                serializer.save(user=request.user.patient,hospital=doctor.hospital)
                return Response({"status": 1, "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"status": 0, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"status": 0,"data":"Something went wrong"}, status=status.HTTP_404_NOT_FOUND)




class AvailableSlotsAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, doctor_id, day, *args, **kwargs):
        # Get all time slots for the given day and doctor
        all_time_slots = [
            {"time": choice[0], "is_booked": False}
            for choice in TIME_CHOICES
        ]
        # Mark booked time slots as "is_booked: True"
        booked_slots = Appointment.objects.filter(doctor_id=doctor_id, day=day)
        for booked_slot in booked_slots:
            time = booked_slot.time
            for slot in all_time_slots:
                if slot["time"] == time:
                    slot["is_booked"] = True

        serializer = AvailableSlotsSerializer(all_time_slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListPatientAppointmentsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPatientUser]
    def get(self, request, *args, **kwargs):
        try:
            appointments = Appointment.objects.filter(user=request.user.patient)
            serializer = AppointmentSerializer(appointments, many=True)
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"status":0,"data":"Something went wrong"}, status=status.HTTP_404_NOT_FOUND)

class CancelAppointmentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPatientUser]
    def delete(self, request, appointment_id, *args, **kwargs):
        # Check if the appointment exists
        try:
            appointment = Appointment.objects.get(id=appointment_id, user=request.user.patient)
        except Appointment.DoesNotExist:
            return Response({"status":0,"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the appointment
        appointment.delete()
        return Response({"status":1,"success": "Appointment canceled successfully."}, status=status.HTTP_204_NO_CONTENT)


class PatientPrescriptionsListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPatientUser]
    def get(self, request):
        try:
            patient = request.user.patient
            prescription = Prescription.objects.filter(patient=patient)
            serializer = PrescriptionSerializer(prescription, many=True)
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)