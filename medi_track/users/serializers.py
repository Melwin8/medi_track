from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .validators import validate_password_complexity,validate_email,validate_username
class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password_complexity])
    email = serializers.EmailField(required=True, validators=[validate_email])
    username = serializers.CharField(required=True, validators=[validate_username])
    class Meta:
        model = CustomUser
        fields = ['username', 'email','password',]

    def create(self, validated_data):
        user=CustomUser.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class HospitalSerializer(serializers.ModelSerializer):

    user = AdminSerializer()
    class Meta:
        model = Hospital
        fields = ['id','user','address','phone_number','contact_information']
    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = CustomUser.objects.create(username=user_data["username"], email=user_data['email'])
        user.set_password(user_data['password'])
        user.is_hospital = True
        user.save()
        hospital = Hospital.objects.create(user=user, **validated_data)
        hospital.name=user.username
        hospital.save()
        return hospital

class DoctorSerializer(serializers.ModelSerializer):
    user = AdminSerializer()
    class Meta:
        model = Doctor
        fields = ['id','user','specialization','department','degree','consultant_type']

    def create(self, validated_data):
        try:
            current_user = self.context['request'].user
            user_data = validated_data.pop('user')
            user = CustomUser.objects.create(username=user_data["username"], email=user_data['email'])
            user.set_password(user_data['password'])
            user.is_doctor = True
            user.save()
            print(current_user,user)
            doctor = Doctor.objects.create(user=user,hospital=current_user.hospital, **validated_data)
            doctor.name = user.username
            doctor.save()
            return doctor
        except:
            pass


class PatientSerializer(serializers.ModelSerializer):
    user = AdminSerializer()
    class Meta:
        model = Patient
        fields = ['id','user',]

    def create(self, validated_data):

        user_data=validated_data.pop('user')
        user=CustomUser.objects.create(username=user_data["username"],email=user_data['email'])
        user.set_password(user_data['password'])
        user.is_patient=True
        user.save()
        patient=Patient.objects.create(user=user, **validated_data)
        patient.name = user.username
        patient.save()
        return patient


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': {'Custom message': ' No active account found with the given credentials'},
        'blank_email': 'Custom message: Please fill in all required fields.',
    }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # adding custom claims
        token['username'] = user.username
        token["email"] = user.email
        token['is_superuser'] = user.is_superuser
        token['is_hospital'] = user.is_hospital
        token['is_doctor'] = user.is_doctor
        token['is_patient'] = user.is_patient
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user:
            data["username"] = user.username
            data["email"] = user.email
            data["is_superuser"] = user.is_superuser
            data['is_hospital'] = user.is_hospital
            data['is_doctor'] = user.is_doctor
            data['is_patient'] = user.is_patient
            return data
        else:
            raise serializers.ValidationError("Only users are allowed to log in here.")




class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']

class listDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"