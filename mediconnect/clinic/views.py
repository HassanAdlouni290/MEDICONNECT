from django.shortcuts import render,redirect
from .models import Patient,Appointment,MedicalRecord
from django.contrib.auth.models import User
from .models import Patient


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




def view_medical_records(request):
    medical_records = MedicalRecord.objects.all()
    context = {'medical_records': medical_records}
    return render(request, 'view_medical_records.html', context)
