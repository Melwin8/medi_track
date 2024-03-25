from rest_framework import fields,serializers
from .models import *
from users.serializers import (PatientSerializer,DoctorSerializer,HospitalSerializer)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from patient.serializers import (AppointmentSerializer)
class PrescriptionMedicineSerializer(serializers.ModelSerializer):
    times = serializers.ListField()
    # times_display = serializers.SerializerMethodField()
    class Meta:
        model = PrescriptionMedicine
        fields = ['id', 'medicine_name', 'dosage', 'times','condition', 'start_date', 'duration','end_date',]
        read_only_fields = ['end_date', ]

    # def get_times_display(self, obj):
    #     time_labels = dict(obj.time_choices)
    #     # return [time_labels[time_value] for time_value in obj.times]
    #     return [(time_value,time_labels[time_value]) for time_value in obj.times]



class PrescriptionSerializer(serializers.ModelSerializer):
    medicines = PrescriptionMedicineSerializer(many=True)

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'doctor', 'appointment', 'hospital', 'medicines','advice', 'created_at']
        read_only_fields = ['patient','hospital','doctor','appointment',]


    def create(self, validated_data):
        medicines_data = validated_data.pop('medicines', [])
        prescription = Prescription.objects.create(**validated_data)
        print(prescription)
        for medicine_data in medicines_data:

            medicine = PrescriptionMedicine.objects.create(prescription=prescription, **medicine_data)

            prescription.medicines.add(medicine)
        return prescription


class DetailedPrescriptionSerializer(serializers.ModelSerializer):
    medicines = PrescriptionMedicineSerializer(many=True)
    patient=serializers.SerializerMethodField()
    doctor=serializers.SerializerMethodField()
    appointment=serializers.SerializerMethodField()
    hospital=serializers.SerializerMethodField()
    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'doctor', 'appointment', 'hospital', 'medicines', 'created_at']
        read_only_fields = ['patient','hospital','doctor','appointment',]

    def get_patient(self, obj):
        return {'id': obj.patient.id, 'name': obj.patient.name}

    def get_doctor(self, obj):
        return {'id': obj.doctor.id, 'name': obj.doctor.name}

    def get_hospital(self, obj):
        return {'id': obj.hospital.id, 'name': obj.hospital.name}
    def get_appointment(self, obj):
        return {'id': obj.appointment.id, 'name': obj.appointment.full_name,'age': obj.appointment.age,'gender': obj.appointment.gender}