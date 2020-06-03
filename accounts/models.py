from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

class MyUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #image = models.ImageField(upload_to='profile_pictures',null=True)
    nationalId = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
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
    bloodGroup = models.CharField(max_length=5 , choices=TYPE_CHOICES, default='A+')
    TYPE_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=10 , choices=TYPE_CHOICES, default='M')
    dob = models.DateField(help_text = 'YYYY-MM-DD',null=True)
    TYPE_CHOICES = [
        ('D', 'Doctor'),
        ('P', 'Patient'),
        ('A', 'Assitant'),
        ('T', 'Technician'),
    ]
    
    userType = models.CharField(max_length=10,choices=TYPE_CHOICES, default='P')
    additionalDetails = models.CharField(max_length=100)
    ratSum = models.FloatField(default=0)
    ratCnt = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def createMyUser(sender, instance, created, **kwargs):
        if created:
            MyUser.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def saveMyUser(sender, instance, **kwargs):
        instance.myuser.save()
        if instance.myuser.userType == 'P':
            try:
                instance.patient
            except ObjectDoesNotExist:
                Patient.objects.create(user=instance)
                Assistant.objects.filter(user=instance).delete()
                Doctor.objects.filter(user=instance).delete()
                Technician.objects.filter(user=instance).delete()

            instance.patient.save()

        if instance.myuser.userType == 'D':

            try:
                instance.doctor
            except ObjectDoesNotExist:
                Doctor.objects.create(user=instance)
                Assistant.objects.filter(user=instance).delete()
                Patient.objects.filter(user=instance).delete()
                Technician.objects.filter(user=instance).delete()

            instance.doctor.save()

        if instance.myuser.userType == 'A':

            try:
                instance.assistant
            except ObjectDoesNotExist:
                Assistant.objects.create(user=instance)
                Doctor.objects.filter(user=instance).delete()
                Patient.objects.filter(user=instance).delete()
                Technician.objects.filter(user=instance).delete()

            instance.assistant.save()

        if instance.myuser.userType == 'T':

            try:
                instance.technician
            except ObjectDoesNotExist:
                Technician.objects.create(user=instance)
                Doctor.objects.filter(user=instance).delete()
                Patient.objects.filter(user=instance).delete()
                Assistant.objects.filter(user=instance).delete()

            instance.technician.save()


    def save(self, *args, **kwargs):

        if self.userType == 'P' :
            table = Patient.objects.filter(user=self.user)
            if len(table) == 0 :
                Patient.objects.create(user=self.user)
            Doctor.objects.filter(user=self.user).delete()
            Assistant.objects.filter(user=self.user).delete()
            Technician.objects.filter(user=self.user).delete()

        if self.userType == 'D' :
            table = Doctor.objects.filter(user=self.user)
            if len(table) == 0 :
                Doctor.objects.create(user=self.user)
            Patient.objects.filter(user=self.user).delete()
            Assistant.objects.filter(user=self.user).delete()
            Technician.objects.filter(user=self.user).delete()

        if self.userType == 'A' :
            table = Assistant.objects.filter(user=self.user)
            if len(table) == 0 :
                Assistant.objects.create(user=self.user)
            Doctor.objects.filter(user=self.user).delete()
            Patient.objects.filter(user=self.user).delete()
            Technician.objects.filter(user=self.user).delete()

        if self.userType == 'T' :
            table = Technician.objects.filter(user=self.user)
            if len(table) == 0 :
                Technician.objects.create(user=self.user)
            Doctor.objects.filter(user=self.user).delete()
            Patient.objects.filter(user=self.user).delete()
            Assistant.objects.filter(user=self.user).delete()


        models.Model.save(self, *args, **kwargs)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dateBecamePatient = models.DateField(help_text='YYYY-MM-DD',null=True)
    def __str__(self):
        return self.user.username

class City(models.Model) :
    name = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name

class Area(models.Model) :
    name = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name

class CityAreaMapping(models.Model) :
    city = models.ForeignKey(City,null=True,on_delete=models.CASCADE)
    area = models.ForeignKey(Area, null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.area.name + " , " + self.city.name

    class Meta:
        unique_together = (('city','area'),)
        ordering = ['city']


class Schedule(models.Model) :
    zone = models.ForeignKey(CityAreaMapping,null=True,on_delete=models.CASCADE)
    road = models.CharField(max_length=100, null=True)
    TYPE_CHOICES = [
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]

    day = models.CharField(max_length=10, choices=TYPE_CHOICES,null=True)
    startTime = models.TimeField(null=True)
    endTime = models.TimeField(null=True)
    def __str__(self):
        return self.zone.__str__() + " " + self.startTime.__str__() + " " + self.endTime.__str__()

    class Meta:
        ordering = ['day']



class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    appointmentsPerDay = models.IntegerField(null=True)
    experience = models.CharField(max_length=100,null=True)
    education = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.user.username

class DoctorScheduleMapping(models.Model) :
    doctor = models.ForeignKey(Doctor,null=True,on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.doctor.__str__() + " " + self.schedule.__str__()


class Assistant(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Technician(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.user.username
        


class DoctorAssistantMapping(models.Model) :
    doctor = models.ForeignKey(Doctor, null=True,on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.doctor.__str__() + " " + self.assistant.__str__()

class Appointment(models.Model) :
    patient = models.ForeignKey(Patient, null=True,on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, null=True,on_delete=models.CASCADE)
    dsm = models.ForeignKey(DoctorScheduleMapping,null=True,on_delete=models.CASCADE)
    dateOfApp = models.DateField(help_text='YYYY-MM-DD')
    dateOfIssue = models.DateField(help_text='YYYY-MM-DD')

    TYPE_CHOICES = [
        ('D', 'Done'),
        ('P', 'Pending'),
    ]
    status = models.CharField(max_length=10, choices=TYPE_CHOICES, default='P')

    
    def __str__(self):
        return self.patient.user.username + " " + self.dateOfApp.__str__()
    

    class Meta:
        ordering = ['dateOfApp']


class Record(models.Model) :
    appointment = models.ForeignKey(Appointment, null=True,on_delete=models.CASCADE)
    symptoms = models.CharField(max_length=100,null=True)
    diseases = models.CharField(max_length=100,null=True)
    addInfo = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.appointment.__str__()


class Access(models.Model) :
    record = models.ForeignKey(Record,null=True,on_delete=models.CASCADE)
    recipient = models.ForeignKey(User,null=True,on_delete=models.CASCADE)

class Review(models.Model) :
    reviewer = models.ForeignKey(User, null=True,related_name='reviewer',on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, null=True,related_name='recipient',on_delete=models.CASCADE)
    rating = models.FloatField()
    text = models.CharField(max_length=100)


class Medicine(models.Model) :
    name = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)
    genericName = models.CharField(max_length=1000)
    manufacturer = models.CharField(max_length=1000)
    addInfo = models.CharField(max_length=1000)
    amount = models.IntegerField(default=-1)


    def __str__(self):
        return self.name + " " + self.type + " " + self.genericName

    class Meta:
        ordering = ['name']

class PrescribedMedicine(models.Model) :
    record = models.ForeignKey(Record,null=True,on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, null=True,on_delete=models.CASCADE)
    addInfo = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    def __str__(self):
        return self.record.__str__() + " " + self.medicine.__str__()


class MedicalProcedure(models.Model) :
    name = models.CharField(max_length=50)
    addInfo = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Report(models.Model) :
    record = models.ForeignKey(Record, null=True,on_delete=models.CASCADE)
    procedure = models.ForeignKey(MedicalProcedure, null=True,on_delete=models.CASCADE)
    result = models.CharField(null=True,max_length=100,default='0')
    addInfo = models.CharField(null=True,max_length=100)

    token = models.CharField(max_length=100,unique=True,default=str(id))

    file = models.FileField(upload_to='reports', null=True)

    TYPE_CHOICES = [
        ('U', 'Uploaded'),
        ('P', 'Pending'),
    ]
    status = models.CharField(max_length=10, choices=TYPE_CHOICES, default='P')

    def __str__(self):
        return self.record.__str__() + " " + self.procedure.__str__()

class AppointmentRequest(models.Model) :
    patient = models.ForeignKey(Patient, null=True,on_delete=models.CASCADE)
    dsm = models.ForeignKey(DoctorScheduleMapping, null=True,on_delete=models.CASCADE)
    dateOfApp = models.DateField(help_text='YYYY-MM-DD')
    dateOfIssue = models.DateField(help_text='YYYY-MM-DD')
    
    
    def __str__(self):
        return self.dsm.doctor.user.username + " " + self.patient.user.username + " " + self.dateOfApp.__str__()
    
    class Meta:
        unique_together = (('patient','dsm','dateOfApp'),)

class AssistantshipRequest(models.Model) :
    doctor = models.ForeignKey(Doctor, null=True,on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, null=True,on_delete=models.CASCADE)
    additionalDetails = models.CharField(max_length=10,null=True)
    def __str__(self):
        return self.doctor.user.username + " " + self.assistant.user.username

    class Meta:
        unique_together = (('doctor','assistant'),)


class Contact(models.Model) :
    username = models.CharField(max_length=10,null=True) 
    name = models.CharField(max_length=10,null=True)
    message = models.CharField(max_length=10,null=True)
    email = models.EmailField()
    date = models.DateField()
    
    def __str__(self):
        return self.name + " " + self.message

