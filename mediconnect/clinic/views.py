from django.shortcuts import render,redirect, HttpResponse
from .models import Patient,Appointment,MedicalRecord
from django.contrib.auth.models import User
from .models import Patient,Doctor,Nurse
import requests
from django.core.mail import EmailMessage



def home(request):
    return render(request, 'home.html')



def register_patient(request):
    if request.method == 'POST':
        # Retrieve the form data from the request.POST dictionary
        username = request.POST['username']
        password = request.POST['password']
        dob = request.POST['dob']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']

        # Create a new User instance
        user = User.objects.create_user(username=username, password=password)

        # Create a new Patient instance and associate it with the User
        patient = Patient.objects.create(user=user, dob=dob, address=address, phone=phone, email=email)

        # Redirect to a success page or another view
        return redirect('success')
    else:
        return render(request, 'register_patient.html')

def success(request):
    return render(request, 'success.html')

def schedule_appointment(request):
    if request.method == 'POST':
        # Retrieve the form data from the request.POST dictionary
        doctor_username = request.POST['Doctor']
        nurse_username = request.POST['Nurse']
        appointment_date = request.POST['appointment_date']
        appointment_time = request.POST['appointment_time']
        treatment = request.POST['treatment']

        # Retrieve the doctor, nurse, and patient based on the usernames
        doctor = User.objects.get(username=doctor_username).doctor
        nurse = User.objects.get(username=nurse_username).nurse
        patient = request.user.patient

        # Create a new Appointment instance
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            nurse=nurse,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            treatment=treatment
        )

        # Redirect to a success page or another view
        return redirect('success')
    else:
        return render(request, 'schedule_appointment.html')


def view_medical_records(request):
    medical_records = MedicalRecord.objects.all()
    context = {'medical_records': medical_records}
    return render(request, 'view_medical_records.html', context)




def schedule_appointment_with_calendly(doctor_email, appointment_date, appointment_time):
    api_token = 'VRE7RLUFMYNSDKCXZ6MEPVWC3SMABIR2'
    base_url = 'https://api.calendly.com'
    event_type_slug = 'One-on-One'

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    # Get the available time slots for the doctor's event type
    availability_url = f'{base_url}/scheduling/event_types/{event_type_slug}/availability'
    response = requests.get(availability_url, headers=headers, params={'date': appointment_date})
    available_slots = response.json()['data']['attributes']['slots']

    # Find the desired time slot
    desired_slot = None
    for slot in available_slots:
        if slot['start_time'].split('T')[1] == appointment_time:
            desired_slot = slot
            break

    if not desired_slot:
        raise ValueError('The requested time slot is not available.')

    # Schedule the appointment
    scheduling_url = f'{base_url}/scheduling/event_requests'
    payload = {
        'event': {
            'event_type_slug': event_type_slug,
            'invitee': {
                'email': doctor_email
            },
            'start_time': desired_slot['start_time'],
            'end_time': desired_slot['end_time'],
        }
    }
    response = requests.post(scheduling_url, headers=headers, json=payload)

    if response.status_code == 201:
        return response.json()['data']['attributes']['uri']
    else:
        raise Exception('Failed to schedule the appointment with Calendly.')



