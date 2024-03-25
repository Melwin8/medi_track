from django.db import models
from users.models import Patient,Doctor,CustomUser,Hospital
# Create your models here.


TIME_CHOICES = [
        ("10:00 AM", "10:00 AM"),
        ("10:30 AM", "10:30 AM"),
        ("11:00 AM", "11:00 AM"),
        ("11:30 AM", "11:30 AM"),
        ("12:00 PM", "12:00 PM"),
        ("12:30 PM", "12:30 PM"),
        ("02:00 PM", "02:00 PM"),
        ("02:30 PM", "02:30 PM"),
        ("03:00 PM", "03:00 PM"),
        ("03:30 PM", "03:30 PM"),
        ("04:00 PM", "04:00 PM"),
        ("04:30 PM", "04:30 PM"),
    ]
class Appointment(models.Model):
    user = models.ForeignKey(Patient, on_delete=models.CASCADE,)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    day = models.DateField()
    time = models.CharField(max_length=10, choices=TIME_CHOICES)
    illness = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.name} doctor: {self.doctor.name}| day: {self.day} | time: {self.time}"