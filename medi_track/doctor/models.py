from django.db import models
from users.models import (Patient,Doctor,Hospital,CustomUser)
from patient.models import (Appointment)
from django.utils import timezone
from multiselectfield.utils import get_max_length
from multiselectfield import MultiSelectField as MSField

class MultiSelectField(MSField):
    def _get_flatchoices(self):
        flat_choices = super(models.CharField, self).flatchoices

        class MSFFlatchoices(list):
            # Used to trick django.contrib.admin.utils.display_for_field into
            # not treating the list of values as a dictionary key (which errors
            # out)
            def __bool__(self):
                return False
            __nonzero__ = __bool__
        return MSFFlatchoices(flat_choices)
    flatchoices = property(_get_flatchoices)


class PrescriptionMedicine(models.Model):
    time_choices = [

        ("08:00:00", 'Morning'),
        ("13:00:00", 'After Noon'),
        ("20:00:00", 'Night'),
    ]
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE,)
    medicine_name = models.CharField(max_length=100)
    # times = MultiSelectField(max_length=10000,choices=time_choices,)
    times=models.JSONField(default=list)
    condition = models.CharField(max_length=20, )
    dosage = models.CharField(max_length=100, default=1)
    start_date = models.DateTimeField(default=timezone.now)
    duration = models.PositiveIntegerField()
    def calculate_end_date(self):
        return self.start_date + timezone.timedelta(days=self.duration)
    @property
    def end_date(self):
        return self.calculate_end_date()

    def __str__(self):
        return f"{self.medicine_name}-{self.prescription}"



class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    medicines = models.ManyToManyField(PrescriptionMedicine,related_name='pre_medicines')
    created_at = models.DateTimeField(default=timezone.now)
    advice = models.TextField(blank=True)

    def __str__(self):
        return f"Prescription for {self.patient.name} by Dr. {self.doctor.name}"
<<<<<<< HEAD
    
    
class Notification(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    content = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
=======
>>>>>>> 1e14084bebf544b132c260d8daedbbdafc2520c8

