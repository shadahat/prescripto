from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.utils.timezone import datetime
from django.contrib.auth.views import login, logout
from heapq import *
from datetime import date,timedelta
from fuzzywuzzy import fuzz
from django.contrib import messages
from django.contrib.auth import authenticate, login


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    
    z = merge_dicts(a, b, c, d, e, f, g) 
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def merge_message(request,args):
    if 'type' in request.session :
        cur = {'notification' : {'type': request.session['type'], 'msg':request.session['message']}}
        del request.session['type']
        del request.session['message']
        return merge_dicts(args,cur)
    else :
        return args

def add_message(request,type,msg):
    request.session['type'] = type
    request.session['message'] = msg


# returns all the records of a patient
# Type List of dictionary
# {'record': record, 'medicines' : meds, 'reports' : reps}
def get_records(patient) :
    records = []
    recs = Record.objects.all()
    for rec in recs:
        if rec.appointment.patient == patient :

            meds = PrescribedMedicine.objects.all().filter(record=rec)
            reps = Report.objects.all().filter(record=rec)

            dic = { 'record' : rec , 'medicines' : meds , 'reports' : reps }
            records.append(dic)
    return records


# Returns a list of appointments
def get_appointments(patient) :
    apps = Appointment.objects.filter(patient=patient)
    ret = []
    for a in apps :
        if a.dateOfApp >= datetime.today().date() :
            ret.append(a)
    return ret

def get_appointment_requests(request) :
    dsm = DoctorAssistantMapping.objects.all().filter(assistant_id=request.user.assistant.id)
    ret = []
    for d in dsm :
        t_app = AppointmentRequest.objects.all()
        for a in t_app :
            if a.dsm.doctor.id == d.doctor.id :
                ret.append(a)
    return ret

def get_friend_requests(request) :
    fr = AssistantshipRequest.objects.all().filter(doctor_id=request.user.doctor.id)
    return fr

def patient_dict(request):
    args = {'user': request.user,'records' : get_records(request.user.patient) , 'appointments' : get_appointments(request.user.patient)}
    return args


def get_schedules(doc):
    data = DoctorScheduleMapping.objects.filter(doctor=doc)
    return data

def doctor_dict(request):
    dam = DoctorAssistantMapping.objects.filter(doctor_id=request.user.doctor.id)
    assistants = []
    for d in dam :
        assistants.append(d.assistant)

    appointments = Appointment.objects.all().filter(dateOfApp=datetime.today().date())
    apps = []
    for a in appointments :
        if a.dsm.doctor.user == request.user :
            apps.append({'appointment': a, 'data': get_records(a.patient)})

    medicine = Medicine.objects.all()
    proc = MedicalProcedure.objects.all()
    cities = City.objects.all()
    areas = Area.objects.all()
    args = {'user': request.user, 'assistants' : assistants , 'apps': apps, 'medicine': medicine, 'proc': proc, 'requests': get_friend_requests(request), 'dsm' : get_schedules(request.user.doctor), 'zones' : CityAreaMapping.objects.all() }
    return args

def assistant_dict(request):
    u = DoctorAssistantMapping.objects.all().filter(assistant_id=request.user.assistant.id)
    doctors = []
    for us in u:
        d = Doctor.objects.get(id=us.doctor_id)

        print(d.user.first_name)

        apps_today = Appointment.objects.all().filter(dateOfApp=datetime.today().date())

        today = 0
        attended = 0

        for app in apps_today :
            if app.dsm.doctor.id == d.id :
                today += 1
                if app.status == 'D' :
                    attended += 1
            

        slist = []

        dsmd = DoctorScheduleMapping.objects.filter(doctor_id=d.id)
        temp = Appointment.objects.all()
        date_today = datetime.today().date()

        for i in range(0, 30):
            for x in dsmd :
                cur = date_today + timedelta(days=i)
                
                number_of_apps_that_day = 0
                
                for t in temp :
                    if t.dsm.doctor == x.doctor and t.dateOfApp == cur :
                        number_of_apps_that_day += 1

                number_of_apps_that_day = x.doctor.appointmentsPerDay - number_of_apps_that_day

                if get_day( cur ) == x.schedule.day :
                    slist.append( {'schedule' : x.schedule, 'date' : cur, 'dsmid' : x.id,'nap' : number_of_apps_that_day} )

        dic = { 'doctor' : d , 'issued_apps_today': today , 'appointments_attended': attended,'schedule' : slist}

        doctors.append(dic)

    a = User.objects.get(id=request.user.id)

    args = {'user': request.user, 'doctors': doctors, 'requests': get_appointment_requests(request)}
    
    return args

def technician_dict(request):
    return {'user' : request.user }

def my_logout(request):
    logout(request)
    return render(request, 'accounts/index.html')


def home(request):
    return render(request, 'accounts/index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            add_message(request,'S','Account Created successfully.')
            return redirect(reverse('edit_profile'))
        else :            
            args = {'form' : form}
            return render(request, 'accounts/reg_form.html', args)
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)

@login_required
def view_profile(request):
    if request.user.myuser.userType == 'P':
        args = patient_dict(request)
        args = merge_message(request,args)
        return render(request, 'accounts/profile_patient.html', args)

    elif request.user.myuser.userType == 'D':
        args = doctor_dict(request)
        args = merge_message(request,args)
        return render(request, 'accounts/profile_doctor.html', args)

    elif request.user.myuser.userType == 'A':
        args = assistant_dict(request)
        args = merge_message(request,args)
        return render(request, 'accounts/profile_assistant.html', args)

    elif request.user.myuser.userType == 'T':
        args = technician_dict(request)
        args = merge_message(request,args)
        return render(request, 'accounts/profile_technician.html', args)


def get_day(d) :
    d0 = date(2018, 4, 24)
    d1 = d
    delta = d1 - d0
    if delta.days % 7 == 0 :
        return "Tuesday"
    if delta.days % 7 == 1 :
        return "Wednesday"
    if delta.days % 7 == 2 :
        return "Thursday"
    if delta.days % 7 == 3 :
        return "Friday"
    if delta.days % 7 == 4 :
        return "Saturday"
    if delta.days % 7 == 5 :
        return "Sunday"
    if delta.days % 7 == 6 :
        return "Monday"

@login_required
def view_dashboard(request):
    if request.user.myuser.userType == 'P':
        args = patient_dict(request)
        args = merge_message(request,args)
        return render(request, 'accounts/dashboard_patient.html', args)

    elif request.user.myuser.userType == 'D':
        args = doctor_dict(request)
        args = merge_message(request,args)
        return render(request, 'accounts/dashboard_doctor.html', args)

    elif request.user.myuser.userType == 'A':        
        args = assistant_dict(request)
        args = merge_message(request,args)
        return render(request, 'accounts/dashboard_assistant.html', args)

    elif request.user.myuser.userType == 'T':
        args = technician_dict(request)
        args = merge_message(request,args)
        return render(request, 'accounts/dashboard_technician.html', args)

def save_patient(request, form):
    user = request.user
    user.first_name = form.cleaned_data.get('first_name')
    user.last_name = form.cleaned_data.get('last_name')
    user.email = form.cleaned_data.get('email')
    user.myuser.nationalId = form.cleaned_data.get('national_id')
    user.myuser.gender = form.cleaned_data.get('gender')
    user.myuser.blood_group = form.cleaned_data.get('blood_group')
    user.myuser.dob = form.cleaned_data.get('date_of_birth')
    user.myuser.additionalDetails = form.cleaned_data.get('additional_details')
    user.save()
    add_message(request,'S','Profile Updated')

def save_assistant(request, form):
    user = request.user
    user.first_name = form.cleaned_data.get('first_name')
    user.last_name = form.cleaned_data.get('last_name')
    user.email = form.cleaned_data.get('email')
    user.myuser.nationalId = form.cleaned_data.get('national_id')
    user.myuser.gender = form.cleaned_data.get('gender')
    user.myuser.blood_group = form.cleaned_data.get('blood_group')
    user.myuser.dob = form.cleaned_data.get('date_of_birth')
    user.myuser.additionalDetails = form.cleaned_data.get('additional_details')
    user.save()
    add_message(request,'S','Profile Updated')

def save_doctor(request, form):
    user = request.user
    user.first_name = form.cleaned_data.get('first_name')
    user.last_name = form.cleaned_data.get('last_name')
    user.email = form.cleaned_data.get('email')
    user.myuser.nationalId = form.cleaned_data.get('national_id')
    user.myuser.gender = form.cleaned_data.get('gender')
    user.myuser.blood_group = form.cleaned_data.get('blood_group')
    user.myuser.dob = form.cleaned_data.get('date_of_birth')
    user.doctor.appointmentsPerDay = form.cleaned_data.get('appointments_per_day')
    user.doctor.experience = form.cleaned_data.get('experience')
    user.doctor.education = form.cleaned_data.get('speciality')
    user.myuser.additionalDetails = form.cleaned_data.get('additional_details')
    user.save()
    add_message(request,'S','Profile Updated')

def save_technician(request, form):
    user = request.user
    user.first_name = form.cleaned_data.get('first_name')
    user.last_name = form.cleaned_data.get('last_name')
    user.email = form.cleaned_data.get('email')
    user.myuser.nationalId = form.cleaned_data.get('national_id')
    user.myuser.gender = form.cleaned_data.get('gender')
    user.myuser.blood_group = form.cleaned_data.get('blood_group')
    user.myuser.dob = form.cleaned_data.get('date_of_birth')
    user.myuser.additionalDetails = form.cleaned_data.get('additional_details')
    user.technician.institution = form.cleaned_data.get('institution')
    user.save()
    add_message(request,'S','Profile Updated')

def edit_profile(request, message = None):
    if request.method == 'POST':
        if request.user.myuser.userType == 'P':
            form = EditPatientForm(request.POST, instance=request.user)
            if form.is_valid():
                save_patient(request, form)
            else :
                add_message(request,'F','Invalid Input')
            return redirect(reverse('edit_profile'))
        elif request.user.myuser.userType == 'D':
            form = EditDoctorForm(request.POST, instance=request.user)
            if form.is_valid():
                save_doctor(request, form)
            else :
                add_message(request,'F','Invalid Input')
            return redirect(reverse('edit_profile'))
        elif request.user.myuser.userType == 'A':
            form = EditAssistantForm(request.POST, instance=request.user)
            if form.is_valid():
                save_assistant(request, form)
            else :
                add_message(request,'F','Invalid Input')
            return redirect(reverse('edit_profile'))
        elif request.user.myuser.userType == 'T':
            form = EditTechnicianForm(request.POST, instance=request.user)
            if form.is_valid():
                save_technician(request, form)
            else :
                add_message(request,'F','Invalid Input')
            return redirect(reverse('edit_profile'))
    else:
        if request.user.myuser.userType == 'P':
            form = EditPatientForm(instance=request.user)
            args = {'form': form}
            args = merge_dicts( args , patient_dict(request) )
            args = merge_message(request,args)
            return render(request, 'accounts/edit_patient.html', args)
        elif request.user.myuser.userType == 'D':
            form = EditDoctorForm(instance=request.user)
            args = {'form': form}
            args = merge_dicts( args , doctor_dict(request) )
            args = merge_message(request,args)
            print(args)
            return render(request, 'accounts/edit_doctor.html', args)
        elif request.user.myuser.userType == 'A':
            form = EditAssistantForm(instance=request.user)
            args = {'form': form}
            args = merge_dicts( args , assistant_dict(request) )
            args = merge_message(request,args)
            return render(request, 'accounts/edit_assistant.html', args)

        elif request.user.myuser.userType == 'T':
            form = EditTechnicianForm(instance=request.user)
            args = {'form': form}
            args = merge_dicts( args , technician_dict(request) )
            args = merge_message(request,args)
            return render(request, 'accounts/edit_assistant.html', args)

def get_data_for_search(d,key,searchby):
    str = ''
    if searchby == '...' :
        str = d.doctor.user.first_name + " " + d.doctor.user.last_name
        str += " " + (d.schedule.zone.area.name + " " + d.schedule.zone.city.name + " " + d.schedule.road)
        str += " " + d.doctor.education + " " + d.doctor.experience
    elif searchby == 'Search by name' :
        str = d.doctor.user.first_name + " " + d.doctor.user.last_name
    elif searchby == 'Search by location' :
        str += " " + (d.schedule.zone.area.name + " " + d.schedule.zone.city.name + " " + d.schedule.road)
    else :
        str += " " + d.doctor.education + " " + d.doctor.experience
    return str.lower()

def get_priority(key,str) :
    priority = fuzz.token_set_ratio(key,str)
    priority = max(priority,fuzz.token_sort_ratio(key,str))
    priority = max(priority, fuzz.ratio(key, str))
    priority = max(priority, fuzz.partial_ratio(key, str))
    priority = max(priority, fuzz.partial_token_sort_ratio(key, str))
    priority = max(priority, fuzz.partial_token_set_ratio(key, str))

    return priority



def do_once(request,is_there_a_key):
    key = ''
    searchby = ''
    
    if is_there_a_key :
        print(request.POST)
        key = request.POST['data']
        searchby = request.POST['searchby']
        request.session['key'] = key
        request.session['searchby'] = searchby

    else :
        key = request.session['key']
        searchby = request.session['searchby']

    print(key)
    print(searchby)

    dsm = DoctorScheduleMapping.objects.all()
    heap = []
    data = []
    for d in dsm :
        str = get_data_for_search(d,key,searchby)
        key = key.lower()

        priority = get_priority(key,str)

        if priority >= 70 :
            data.append((-1*priority,d.id))

    for item in data:
        heappush(heap, item)

    sorted = []
    while heap:
        sorted.append(DoctorScheduleMapping.objects.get(id=heappop(heap)[1]))

    dlist = []

    for s in sorted :
        dlist.append(s.doctor)

    docs = Doctor.objects.all()

    doctors = []

    for d in docs :
        if d in dlist :
            slist = []
            dsmd = DoctorScheduleMapping.objects.filter(doctor_id=d.id)
            date_today = datetime.today().date()
            for i in range(0, 30):
                for x in dsmd:
                    cur = date_today + timedelta(days=i)
                    if get_day(cur) == x.schedule.day:
                        slist.append({'schedule': x.schedule, 'date': cur, 'dsmid': x.id})

            if request.user.myuser.userType == 'A' :
                t1 = DoctorAssistantMapping.objects.all().filter(doctor_id=d.id).filter(
                    assistant_id=request.user.assistant.id)

                t2 = AssistantshipRequest.objects.all().filter(doctor_id=d.id).filter(
                    assistant_id=request.user.assistant.id)

                flag = 0
                if len(t1) != 0:
                    flag = 2
                elif len(t2) != 0:
                    flag = 1

                ## 0 Send Req
                ## 1 Pending
                ## 2 Friends
                dic = {'doctor': d, 'schedule': slist, 'flag': flag }
            else :
                dic = {'doctor': d, 'schedule': slist }

            doctors.append(dic)

    args = {'docs': doctors, 'key' : key}
    return args

def search(request):
    if request.method == 'POST':

        args = do_once(request,True)
        
        if request.user.myuser.userType == 'P' :
            args = merge_message(request,args)
            args = merge_dicts(args,patient_dict(request))
            return render(request, 'accounts/searched_by_patient.html', args)
        elif request.user.myuser.userType == 'A' :
            args = merge_message(request,args)
            args = merge_dicts(args,assistant_dict(request))
            return render(request, 'accounts/searched_by_assistant.html', args)
        
    else:
        
        args = do_once(request,False)

        if request.user.myuser.userType == 'P' :
            args = merge_message(request,args)
            args = merge_dicts(args,patient_dict(request))
            return render(request, 'accounts/searched_by_patient.html', args)
        elif request.user.myuser.userType == 'A' :
            args = merge_message(request,args)
            args = merge_dicts(args,assistant_dict(request))
            return render(request, 'accounts/searched_by_assistant.html', args)


def get_month(data) :
    if data == "January" :
        return '01'
    if data == "February" :
        return '02'
    if data == "March" :
        return '03'
    if data == "April" :
        return '04'
    if data == "May" :
        return '05'
    if data == "June" :
        return '06'
    if data == "July" :
        return '07'
    if data == "August" :
        return '08'
    if data == "September" :
        return '09'
    if data == "October" :
        return '10'
    if data == "November" :
        return '11'
    if data == "December" :
        return '12'


def parse(now) :
    start = 0
    end = len(now)
    mlist = []
    last = 0
    no = -1
    for i in range(start, end):
        if i == no:
            continue
        elif now[i] == ',':
            mlist.append(now[last:i])
            last = i + 2
            no = i + 1
        elif now[i] == ' ':
            mlist.append(now[last:i])
            last = i + 1
    return  mlist

def check(doc,date):
    apps = Appointment.objects.all()
    len = 0
    for a in apps : 
        if a.dsm.doctor == doc and a.dateOfApp == date :
            len += 1

    if len >= doc.appointmentsPerDay :
        return False
    else :
        return True


def add_appointment(request) :
    if request.method == 'POST': 
        a = Appointment()

        u = ''
        temp = User.objects.all()
        for t in temp :
            if t.myuser.userType == 'P' :
                if t.username == request.POST['pid'] :
                    u = t

        cnt = 0
        temp = Patient.objects.all()
        for t in temp :
            if t.user.username == request.POST['pid'] :
                cnt = 1

        if cnt == 0:
            add_message(request,'F','Wrong username!')
            return redirect(reverse('view_dashboard'))
        
        a.patient = Patient.objects.get(user=u)

        a.assistant = Assistant.objects.get(id=int(request.POST['aid']))
        now = request.POST['selected']
        mlist = parse(now)
        a.dsm = DoctorScheduleMapping.objects.get(id=int(mlist[0]))
        a.dateOfApp = mlist[3] + '-' + get_month(mlist[1]) + '-' + mlist[2]
        a.dateOfIssue = datetime.today().date()
        a.status = 'P'
        
        if check(a.dsm.doctor,a.dateOfApp) :
            msg = 'Appointment for Dr. ' + a.dsm.doctor.user.first_name + ' '  + a.dsm.doctor.user.last_name + ' has ben accepted.'
            add_message(request,'S',msg)
            a.save()
        else :
            msg = 'All slots on ' + a.dateOfApp.__str__() + ' are booked!'
            add_message(request,'F',msg)

        return redirect(reverse('view_dashboard'))

def request_appointment(request):
    if request.method == 'POST':
        print(request.POST)
        a = AppointmentRequest()
        a.patient = Patient.objects.get(id=int(request.POST['pid']))
        now = request.POST['selected']
        mlist = parse(now)
        a.dsm = DoctorScheduleMapping.objects.get(id=int(mlist[0]))
        a.dateOfApp = mlist[3] + '-' + get_month(mlist[1]) + '-' + mlist[2]
        a.dateOfIssue = datetime.today().date()
        a.save()

        msg = 'Appointment request to Dr. ' + a.dsm.doctor.user.first_name + ' '  + a.dsm.doctor.user.last_name 
        msg += ' has ben sent. The appointment will show up on your dashboard when accepted.'
        
        add_message(request,'S',msg)
        return redirect(reverse('search'))

import string
import random
def token_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_token (ls):
    flag = 0
    while flag == 0:
        token = token_generator()
        if token not in ls:
            return token

def create_prescription(request):
    if request.method == 'POST':
        print(request.POST)

        save = 0

        nmeds = int(request.POST['num_of_medicine'])
        nreps = int(request.POST['num_of_report'])

        print(request.POST['appt_id'])

        app = Appointment.objects.get(id=request.POST['appt_id'])
        rec = Record(appointment=app)
        rec.save()

        pre = PrescribedMedicine()
        rep = MedicalProcedure()

        got_med = False
        got_rep = False


        for i in range(0,nmeds) :
            medid = int(request.POST['selected_med'+str(i)])
            med = Medicine.objects.get(id=medid)
            pre = PrescribedMedicine(record=rec,medicine=med,addInfo=request.POST['ai'+str(i)])
            if request.POST['amount'+str(i)] == '' :
                pre.amount = 0
            else :
                pre.amount = request.POST['amount'+str(i)]

            if(med.name != '-------') :
                got_med = True
                pre.save()

        tokens = []
        temp = Report.objects.all()
        for t in temp :
            tokens.append(t.token)

        for i in range(0, nreps):
            repid = int(request.POST['selected_proc' + str(i)])
            proc = MedicalProcedure.objects.get(id=repid)
            ai = request.POST['proc_ai'+str(i)]
            rep = Report(record=rec,procedure=proc,result='',addInfo=ai)

            if (proc.name != '-------') :
                got_rep = True

                new_tok = generate_token(tokens)
                tokens.append(new_tok)

                rep.token = new_tok
                rep.save()



        if got_med or got_rep:
            app.status = 'D'
            app.save()
            rec.save()
        else :
            rec.delete()

        add_message(request,'S','Prescription Saved!')
        return redirect(reverse('view_dashboard'))

def reject_appointment(request):
    if request.method == 'POST':
        AppointmentRequest.objects.filter(id=request.POST['id']).delete()
        add_message(request,'S','Request Deleted!')
        return redirect(reverse('view_dashboard'))

def accept_appointment(request):
    if request.method == 'POST':
        a = Appointment()
        a.patient = Patient.objects.get(id=int(request.POST['pid']))
        now = '1 ' + request.POST['date'] + ' '
        mlist = parse(now)
        a.dsm = DoctorScheduleMapping.objects.get(id=int(request.POST['dsmid']))
        a.dateOfApp = mlist[3] + '-' + get_month(mlist[1]) + '-' + mlist[2]
        a.dateOfIssue = datetime.today().date()
        a.status = 'P'
        a.assistant = request.user.assistant


        if check(a.dsm.doctor,a.dateOfApp) :
            msg = 'Appointment for Dr. ' + a.dsm.doctor.user.first_name + ' '  + a.dsm.doctor.user.last_name + ' has ben accepted.'
            add_message(request,'S',msg)
            a.save()
        else :
            msg = 'All slots on ' + a.dateOfApp.__str__() + ' are booked!'
            add_message(request,'F',msg)

        AppointmentRequest.objects.filter(id=request.POST['id']).delete()
        return redirect(reverse('view_dashboard'))

        

def request_assistant(request):
    if request.method == 'POST':
        print(request.POST)
        a = AssistantshipRequest()
        a.doctor = Doctor.objects.get(id=int(request.POST['did']))
        a.assistant = request.user.assistant
        a.save()

        msg = 'Request sent to Dr. ' + a.doctor.user.first_name + ' ' + a.doctor.user.last_name
        msg += '. He will be on your dashboard when accepted.'
        add_message(request,'S',msg)
        return redirect(reverse('search'))

def reject_assistant(request):
    if request.method == 'POST':
        doc = Doctor.objects.get(id=request.user.doctor.id)
        ass = Assistant.objects.get(id=request.POST['aid'])
        ob = AssistantshipRequest.objects.all().filter(doctor=doc).filter(assistant=ass)
        ob[0].delete()
        msg = 'Request Rejected.'
        add_message(request,'S',msg)
        args = doctor_dict(request)
        return redirect(reverse('view_dashboard'))

def accept_assistant(request):
    if request.method == 'POST':
        doc = Doctor.objects.get(id=request.user.doctor.id)
        ass = Assistant.objects.get(id=request.POST['aid'])
        ob = AssistantshipRequest.objects.all().filter(doctor=doc).filter(assistant=ass)
        print(ob[0])
        DoctorAssistantMapping(doctor=doc,assistant=ass).save()
        ob[0].delete()
        msg = ass.user.first_name + " " + ass.user.last_name + ' is your new Assistant.'
        msg += ' Congratulations!'
        add_message(request,'S',msg)
        args = doctor_dict(request)
        return redirect(reverse('view_dashboard'))

def add_report(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            tk = form.cleaned_data['token']
            temp = Report.objects.all().filter(token=tk)
            if len(temp) == 0 :
                add_message(request,'F','Wrong Token!')
                return redirect(reverse('add_report'))
            rep = Report.objects.get(token=tk)

            if rep.status == 'U' :
                add_message(request,'F','Already Uploaded!')
                return redirect(reverse('add_report'))

            rep.status = 'U'
            rep.file = form.cleaned_data['file']
            rep.save()
            add_message(request,'S','Report is uploaded successfully!')

        else :
            add_message(request,'F','Invalid Input')

        return redirect(reverse('add_report'))

    else :
        form = FileUploadForm()
        args = {'form': form}
        args = merge_dicts( args,technician_dict(request) )
        args = merge_message(request,args)
        return render(request, 'accounts/dashboard_technician.html', args)

def save_message(request):
    if request.method == 'POST' :
        c = Contact()
        if request.user.is_authenticated():
            c.username = request.user.username
        else :
            c.username = ''
        c.name = request.POST['name']
        c.email = request.POST['email']
        c.message = request.POST['message']
        c.date = datetime.today().date()
        c.save()
        add_message(request,'S','Message Sent')
        return redirect(reverse('contact'))

def delete_schedule(request):
    if request.method == 'POST':
        data = DoctorScheduleMapping.objects.get(id=int(request.POST['id']))
        data.delete()
        request.session['type'] = 'S'
        request.session['message'] = 'Schedule Deleted.'
        return redirect(reverse('edit_profile'))

from datetime import time

def get_time(str) :
    h = int(0)
    m = int(0)
    for i in range(0,2) :
        h *= 10
        h += int(str[i])

    for i in range(3,5) :
        m *= 10
        m += int(str[i])

    return time(h,m,0)

def add_schedule(request):
    if request.method == 'POST':
        print(request.POST)
        sch = Schedule()

        sch.zone = CityAreaMapping.objects.get(id=int(request.POST['zone']))
        sch.road = request.POST['road']
        sch.day = request.POST['day']
        sch.startTime = get_time( request.POST['start'] )
        sch.endTime = get_time( request.POST['end'] )

        data = Schedule.objects.filter(zone=sch.zone).filter(day=sch.day).filter(road=sch.road)
        
        ns = str(sch.startTime)
        ne = str(sch.endTime)

        cnt = 0
        for d in data :
            s = str(d.startTime)
            e = str(d.endTime)

            if ns == s and ne == e :
                cnt += 1;
                sch = d

        if cnt == 0 :
            sch.save()
            DoctorScheduleMapping(doctor=Doctor.objects.get(id=int(request.POST['did'])),schedule=sch).save()
            add_message(request,'S','Schedule Added.')
        else :
            if len(DoctorScheduleMapping.objects.filter(doctor=Doctor.objects.get(id=int(request.POST['did']))).filter(schedule=sch)) == 0 :
                DoctorScheduleMapping(doctor=Doctor.objects.get(id=int(request.POST['did'])),schedule=sch).save()
                add_message(request,'S','Schedule Added.')
            else :
                add_message(request,'S','Schedule Already Exists.')        
        return redirect(reverse('edit_profile'))
    else:
        return redirect(reverse('view_profile'))


def location_valid (response):
  return True
  
def speciality_valid (response):
  return True
  
def symptom_valid (response):
  return True

def generateMessage (request, response):
  if request.session['last_message'] == 'lookingfordoctor':
    if 'yes' in response.lower():
      request.session['lookingfor'] = 'yes'
      request.session['last_message'] = 'location'
      return 'In which city do you want to get an appointment?'
    elif 'no' in response.lower():
      request.session['lookingfor'] = 'no'
      return 'Okay, thank you. Thanks for using our service Please let us know if you want anything in future.'
    else:
      return 'Sorry, I could not understand. Do you want an appointment?'
  elif request.session['last_message'] == 'location':
    if location_valid(response):
      request.session['location'] = response
      request.session['last_message'] = 'speciality'
      return 'Which speciality are you looking for?'
    else:
      return 'Sorry, I could not understand you. Can you please be more specific?'
    
  elif request.session['last_message'] == 'speciality':
    if 'no' in response:
      request.session['last_message'] = 'symptom'
      return 'What problems are you facing?'
    elif speciality_valid(response):
      request.session['speciality'] = response
      request.session['last_message'] = 'suggestion'
      return 'Here are some doctors that you might want to consider.'
    else:
      return 'Sorry, I could not understand you. Can you please be more specific?'
  
  
  
  elif request.session['last_message'] == 'symptom':
    if 'no' in response or "don\'t" in response:
      request.session['last_message'] = 'suggestion'
      return 'Here are some doctors that you might want to consider.'
    elif symptom_valid(response):
      request.session['symptom'] = response
      request.session['last_message'] = 'suggestion'
      return 'Here are some doctors that you might want to consider.'
    else:
      return 'Sorry, I could not understand you. Can you please be more specific?'
    
  else:
    pass

def get_for_meena(request,location,speciality,key1,key2,docs) :
    key = key1 + ' ' + key2
    
    dsm = DoctorScheduleMapping.objects.all()
    heap = []
    data = []
    for d in dsm :
        str = ''
        if location :
            str += " " + (d.schedule.zone.area.name + " " + d.schedule.zone.city.name + " " + d.schedule.road)
        if speciality :
            str += " " + d.doctor.education
        str = str.lower()
        key = key.lower()

        priority = get_priority(key,str)

        if priority >= 70 :
            data.append((-1*priority,d.id))

    for item in data:
        heappush(heap, item)

    sorted = []
    while heap:
        sorted.append(DoctorScheduleMapping.objects.get(id=heappop(heap)[1]))

    dlist = []

    for s in sorted :
        dlist.append(s.doctor)

    #docs = Doctor.objects.all()

    doctors = []

    for d in docs :
        if d in dlist :
            slist = []
            dsmd = DoctorScheduleMapping.objects.filter(doctor_id=d.id)
            date_today = datetime.today().date()
            for i in range(0, 30):
                for x in dsmd:
                    cur = date_today + timedelta(days=i)
                    if get_day(cur) == x.schedule.day:
                        slist.append({'schedule': x.schedule, 'date': cur, 'dsmid': x.id})

            if request.user.myuser.userType == 'A' :
                t1 = DoctorAssistantMapping.objects.all().filter(doctor_id=d.id).filter(
                    assistant_id=request.user.assistant.id)

                t2 = AssistantshipRequest.objects.all().filter(doctor_id=d.id).filter(
                    assistant_id=request.user.assistant.id)

                flag = 0
                if len(t1) != 0:
                    flag = 2
                elif len(t2) != 0:
                    flag = 1

                ## 0 Send Req
                ## 1 Pending
                ## 2 Friends
                dic = {'doctor': d, 'schedule': slist, 'flag': flag }
            else :
                dic = {'doctor': d, 'schedule': slist }

            doctors.append(dic)

    args = {'docs': doctors, 'key' : key}
    return args



def suggestions_by_meena (request):
    if 'lookingfor' in request.session and request.session['lookingfor'] == 'yes':
        if 'location' in request.session:
            cur = get_for_meena(request,True,False,request.session['location'],'',Doctor.objects.all())
            list = []
            for d in cur['docs'] : 
                list.append(d['doctor'])

            if 'speciality' in request.session:
                return get_for_meena(request,False,True,'',request.session['speciality'],list)
            else:
                if 'symptom' in request.session:
                    return {}
                else:
                    return get_for_meena(request,True,False,request.session['location'],'',Doctor.objects.all())
        else:
            return {}
    else:
        return {}

def meena(request):
    if request.method == 'POST' and request.POST['type'] == 'sent':
          args= request.session['meena_message']
          name = request.user.first_name + " " + request.user.last_name
          args['meena_messages'].append({ 'sender': name , 'meena_message': request.POST['message'] } )
          generated_message = generateMessage(request, request.POST['message'])
          request.session['meena_message'] = args
          if generated_message == 'Here are some doctors that you might want to consider.':
            cur = suggestions_by_meena(request)
            args = merge_dicts(args,suggestions_by_meena(request))
          args['meena_messages'].append({ 'sender': 'Meena' , 'meena_message': generated_message} )
          
          return render(request,'accounts/meena.html', args)
    else:
        args= {'meena_messages': [{'sender': 'Meena', 'meena_message': 'Hello, welcome to Prescripto.'}, {'sender':'Meena', 'meena_message':'Are you looking for a doctor?'}]}
        request.session['last_message'] = 'lookingfordoctor'
        request.session['meena_message'] = args
        return render(request,'accounts/meena.html', args)
    
