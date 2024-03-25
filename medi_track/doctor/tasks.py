from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone
from .models import *
 

@shared_task(bind=True)
def send_notification_based_on_times(self):
    print("jhuiooooooooooooo")
    now = timezone.now()
    print("jhuiooooooooooooo")
    medicines_to_remind = PrescriptionMedicine.objects.filter(times__contains=now.strftime('%H:%M'))
    for medicine in medicines_to_remind:
        patient = medicine.prescription.patient
        content = f"Don't forget to take {medicine.medicine_name}"
        n=Notification.objects.create(patient=patient, content=content)
        n.save()
        
        
        # devices = FCMDevice.objects.filter(user=medicine.prescription.patient)
        # devices.send_message(title="Medicine Reminder", body=f"Don't forget to take {medicine.medicine_name}")
    print("done")
    
