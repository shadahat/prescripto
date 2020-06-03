from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import *
from django.forms import ModelForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    TYPES = (
        ('P', 'Patient'),
        ('D', 'Doctor'),
        ('A', 'Assistant'),
        ('T', 'Technician'),
    )

    register_as = forms.ChoiceField(required=True,choices=TYPES)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Your email is not unique.')
        else  :
            raise forms.ValidationError('Email can not be empty.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('Your username is not unique.')
        else  :
            raise forms.ValidationError('Username can not be empty.')
        return username




    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.myuser.userType = self.cleaned_data['register_as']
            user.save()

        return user

    


class EditPatientForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    national_id = forms.CharField(required=True)
    TYPE_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(required=True, choices=TYPE_CHOICES)
    TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    blood_group = forms.ChoiceField(required=True, choices=TYPE_CHOICES)
    date_of_birth = forms.DateField(required=True,help_text='Format yyyy-mm-dd')
    additional_details = forms.CharField(required=False)


    def __init__(self, *args, **kwargs) :
        user = kwargs.pop('instance')
        super(EditPatientForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['national_id'].initial = user.myuser.nationalId
        self.fields['date_of_birth'].initial = user.myuser.dob
        self.fields['blood_group'].initial = user.myuser.bloodGroup
        self.fields['additional_details'].initial = user.myuser.additionalDetails


class EditAssistantForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    national_id = forms.CharField(required=True)
    TYPE_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(required=True, choices=TYPE_CHOICES)
    TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    blood_group = forms.ChoiceField(required=True, choices=TYPE_CHOICES)
    date_of_birth = forms.DateField(required=True, help_text='Format yyyy-mm-dd')
    additional_details = forms.CharField(required=False)


    def __init__(self, *args, **kwargs) :
        user = kwargs.pop('instance')
        super(EditAssistantForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['national_id'].initial = user.myuser.nationalId
        self.fields['date_of_birth'].initial = user.myuser.dob
        self.fields['blood_group'].initial = user.myuser.bloodGroup
        self.fields['additional_details'].initial = user.myuser.additionalDetails


class EditDoctorForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    national_id = forms.CharField(required=True)
    TYPE_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(required=True, choices=TYPE_CHOICES)
    TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    blood_group = forms.ChoiceField(required=True, choices=TYPE_CHOICES)
    date_of_birth = forms.DateField(required=True,help_text='Format yyyy-mm-dd')
    additional_details = forms.CharField(required=False)
    appointments_per_day = forms.IntegerField(required=True,min_value=1,help_text='Must be positive integer')
    speciality = forms.CharField(required=True)
    experience = forms.CharField(required=False)

    def __init__(self, *args, **kwargs) :
        user = kwargs.pop('instance')
        super(EditDoctorForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['national_id'].initial = user.myuser.nationalId
        self.fields['date_of_birth'].initial = user.myuser.dob
        self.fields['blood_group'].initial = user.myuser.bloodGroup
        self.fields['additional_details'].initial = user.myuser.additionalDetails
        self.fields['appointments_per_day'].initial = user.doctor.appointmentsPerDay
        self.fields['speciality'].initial = user.doctor.education
        self.fields['experience'].initial = user.doctor.experience



class EditTechnicianForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    national_id = forms.CharField(required=True)
    TYPE_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(required=True, choices=TYPE_CHOICES)
    TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    blood_group = forms.ChoiceField(required=True, choices=TYPE_CHOICES)
    date_of_birth = forms.DateField(required=True,help_text='Format yyyy-mm-dd')
    additional_details = forms.CharField(required=False)
    institution = forms.CharField(required=False)


    def __init__(self, *args, **kwargs) :
        user = kwargs.pop('instance')
        super(EditTechnicianForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['national_id'].initial = user.myuser.nationalId
        self.fields['date_of_birth'].initial = user.myuser.dob
        self.fields['blood_group'].initial = user.myuser.bloodGroup
        self.fields['additional_details'].initial = user.myuser.additionalDetails
        self.fields['institution'].initial = user.technician.institution


class FileUploadForm(forms.Form):
    file = forms.FileField()
    token = forms.CharField()
