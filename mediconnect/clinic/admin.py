from django.contrib import admin
from .models import *

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


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Nurse, NurseAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(MedicalRecord,MedicalRecordAdmin)