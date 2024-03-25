from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)

        try:
            user.validate_unique()
        except ValidationError as e:
            raise ValidationError({'error': 'Username or email already exists.'}) from e

        user.save(using=self._db)
        return user


    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_hospital = models.BooleanField('hr status',default=False)
    is_doctor = models.BooleanField('team_lead status',default=False)
    is_patient = models.BooleanField('employee status',default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Hospital(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    contact_information = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
class Department(models.Model):
    department_name = models.CharField(max_length=255, )
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    def __str__(self):
        return self.department_name

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE,)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    degree = models.CharField(max_length=255, null=True, blank=True)
    consultant_type = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True, blank=True)
    phone_number= models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name




