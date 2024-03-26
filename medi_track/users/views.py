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


# class UserloginView(TokenObtainPairView):
#     serializer_class = UserTokenObtainPairSerializer

# class PatientRegistrationView(generics.CreateAPIView):
#     queryset = Patient.objects.all()
#     serializer_class =PatientSerializer

# class HospitalRegistrationView(generics.CreateAPIView):
#     queryset = Hospital.objects.all()
#     serializer_class = HospitalSerializer

# class DoctorRegistrationView(generics.CreateAPIView):
#     queryset = Doctor.objects.all()
#     serializer_class = DoctorSerializer
#     permission_classes = [IsAuthenticated,IsHospitalUser]

class UserloginView(APIView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                # Perform any additional logic if needed
                return Response({"status": 1, "data": serializer.validated_data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": 0, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": 0, "errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PatientRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = PatientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": 1, "message": "Patient registered successfully."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": 0, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": 0, "errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)       
        

class HospitalRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = HospitalSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": 1, "message": "Hospital registered successfully."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": 0, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": 0, "errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        

class DoctorRegistrationView(APIView):
    permission_classes = [IsAuthenticated, IsHospitalUser]

    def post(self, request, *args, **kwargs):
        try:
            serializer = DoctorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": 1, "message": "Doctor registered successfully."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": 0, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": 0, "errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






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
        except Exception as e:
            return Response({"status": 0, "errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DepartmentListofAuthenticatedHospitalAPIView(APIView):
    permission_classes = [IsAuthenticated, IsHospitalUser]
    def get(self, request, *args, **kwargs):
        try:
            hospital = request.user.hospital

            departments = Department.objects.filter(hospital=hospital)
            serializer = DepartmentSerializer(departments, many=True)
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except Hospital.DoesNotExist:
            return Response({"status": 0, "errors": "Hospital does not exist for the current user."}, status=status.HTTP_404_NOT_FOUND)

class DoctorListofAuthenticatedHospitalAPIView(APIView):
    permission_classes = [IsAuthenticated, IsHospitalUser]
    def get(self, request, *args, **kwargs):
        try:
            hospital = request.user.hospital

            doctors = Doctor.objects.filter(hospital=hospital)
            serializer = listDoctorSerializer(doctors, many=True)
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except Hospital.DoesNotExist:
            return Response({"status": 0, "errors": "not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # return Response("Doctors does not exist for the current user.", status=status.HTTP_404_NOT_FOUND)

class DoctorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, doctor_id, *args, **kwargs):
        try:
            # Retrieve the doctor by ID
            doctor = Doctor.objects.get(pk=doctor_id)
            # Serialize the doctor's data
            serializer = DoctorSerializer(doctor)
            return Response({"status":1,"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": 0, "errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

