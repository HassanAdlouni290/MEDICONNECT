from django.contrib import admin
from django.core.mail import send_mail

from .models import *
from .views import *

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient','date','diagnosis','prescription']

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialty', 'email', 'phone']

class NurseAdmin(admin.ModelAdmin):
    list_display = ['user','phone']

class PatientAdmin(admin.ModelAdmin):
    list_display = ['user','dob','address','phone','email']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient','doctor','nurse','appointment_date','appointment_time','treatment']

    def get_queryset(self, request):
        # Only display appointments for the current user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusers can see all appointments
            return qs
        elif hasattr(request.user, 'doctor'):
            return qs.filter(doctor=request.user.doctor)
        elif hasattr(request.user, 'nurse'):
            return qs.filter(nurse=request.user.nurse)
        elif hasattr(request.user, 'patient'):
            return qs.filter(patient=request.user.patient)
        else:
            # Non-doctor users won't see any appointments
            return qs.none()

    def get_readonly_fields(self, request, obj=None):
        if hasattr(request.user, 'nurse'):
            return self.readonly_fields + ('appointment_date','appointment_time','confirmed',)
        if hasattr(request.user, 'doctor'):
            return self.readonly_fields + ('patient','doctor',)
        return self.readonly_fields

    def send_sms_notifications(modeladmin, request, queryset):
        # Get the selected rows and perform any necessary processing
        selected_rows = list(queryset)

        numbers = ['76920402', '71023219']  # Replace with your desired numbers

        for number in numbers:
            url = f"http://unosms.us/api.php?user=naderbakir@gmail.com&pass=qfzjui&to={number}&from=fsegorg&msg=Hi Hassan"
            response = requests.get(url)

            if response.status_code == 200:
                print(f"SMS sent to {number} successfully!")
            else:
                print(f"Failed to send SMS to {number}. Error: {response.text}")

    def send_email_notifications(modeladmin, request, queryset):
        # Get the selected rows and perform any necessary processing
        selected_rows = list(queryset)

        for appointment in selected_rows:
            recipient = appointment.patient.email

            subject = 'Notification'
            message = 'Hi, this is a notification email.'
            from_email = 'hasanadlouni@gmail.com'  # Replace with your email address or use a valid email from the settings
            recipient_list = [recipient]

            try:
                send_mail(subject, message, from_email, recipient_list)
                print(f"Email sent to {recipient} successfully!")
            except Exception as e:
                print(f"Failed to send email to {recipient}. Error: {str(e)}")

    send_email_notifications.short_description = "Send email notifications"

    actions = [send_sms_notifications, send_email_notifications]


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Nurse, NurseAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(MedicalRecord,MedicalRecordAdmin)