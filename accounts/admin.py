from django.contrib import admin

from accounts.models import *

# Re-register UserAdmin
admin.site.register(Contact)
admin.site.register(MyUser)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Assistant)
admin.site.register(Technician)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(CityAreaMapping)
admin.site.register(Schedule)
admin.site.register(DoctorScheduleMapping)
admin.site.register(Appointment)
admin.site.register(DoctorAssistantMapping)
admin.site.register(Record)
admin.site.register(Access)
admin.site.register(Review)
admin.site.register(MedicalProcedure)
admin.site.register(Medicine)
admin.site.register(PrescribedMedicine)
admin.site.register(Report)
admin.site.register(AppointmentRequest)
admin.site.register(AssistantshipRequest)
