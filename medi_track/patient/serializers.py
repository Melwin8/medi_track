from rest_framework import serializers
from users.models import (Hospital,Doctor,CustomUser)
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']
class AllHospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = "__all__"

class DoctorsSerializer(serializers.ModelSerializer):
    hospital = AllHospitalSerializer()
    class Meta:
        model = Doctor
        fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id','user','doctor','hospital', 'full_name', 'age', 'gender', 'day', 'time', 'illness', 'time_created']
        read_only_fields = ['user','hospital', 'time_created',]


class AvailableSlotsSerializer(serializers.Serializer):
    time = serializers.CharField()
    is_booked = serializers.BooleanField()


