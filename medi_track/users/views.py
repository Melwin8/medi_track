from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics,mixins
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .permissions import IsHospitalUser, IsDoctorUser, IsPatientUser
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.


class UserloginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

class PatientRegistrationView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class =PatientSerializer

class HospitalRegistrationView(generics.CreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class DoctorRegistrationView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated,IsHospitalUser]





class DepartmentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated,IsHospitalUser]

    def post(self, request, *args, **kwargs):

        try:
            # Retrieve the hospital associated with the authenticated user
            hospital = request.user.hospital
            serializer = DepartmentSerializer(data=request.data)
            if serializer.is_valid():
                # Automatically associate the department with the hospital
                serializer.save(hospital=hospital)
                return Response({"status":1,"data":serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"status":0,"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Something went wrong.", status=status.HTTP_404_NOT_FOUND)

class DepartmentListofAuthenticatedHospitalAPIView(APIView):
    permission_classes = [IsAuthenticated, IsHospitalUser]
    def get(self, request, *args, **kwargs):
        try:
            hospital = request.user.hospital

            departments = Department.objects.filter(hospital=hospital)
            serializer = DepartmentSerializer(departments, many=True)
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except Hospital.DoesNotExist:
            return Response("Hospital does not exist for the current user.", status=status.HTTP_404_NOT_FOUND)

class DoctorListofAuthenticatedHospitalAPIView(APIView):
    permission_classes = [IsAuthenticated, IsHospitalUser]
    def get(self, request, *args, **kwargs):
        try:
            hospital = request.user.hospital

            doctors = Doctor.objects.filter(hospital=hospital)
            serializer = listDoctorSerializer(doctors, many=True)
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except Hospital.DoesNotExist:
            return Response("Doctors does not exist for the current user.", status=status.HTTP_404_NOT_FOUND)

class DoctorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, doctor_id, *args, **kwargs):
        try:
            # Retrieve the doctor by ID
            doctor = Doctor.objects.get(pk=doctor_id)
            # Serialize the doctor's data
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response("Doctor not found.", status=status.HTTP_404_NOT_FOUND)

