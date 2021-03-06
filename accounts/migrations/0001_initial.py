# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-01 10:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateOfApp', models.DateField(help_text='YYYY-MM-DD')),
                ('dateOfIssue', models.DateField(help_text='YYYY-MM-DD')),
                ('status', models.CharField(choices=[('D', 'Done'), ('P', 'Pending')], default='P', max_length=10)),
            ],
            options={
                'ordering': ['dateOfApp'],
            },
        ),
        migrations.CreateModel(
            name='AppointmentRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateOfApp', models.DateField(help_text='YYYY-MM-DD')),
                ('dateOfIssue', models.DateField(help_text='YYYY-MM-DD')),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Assistant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AssistantshipRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additionalDetails', models.CharField(max_length=10, null=True)),
                ('assistant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Assistant')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CityAreaMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Area')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.City')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointmentsPerDay', models.IntegerField(null=True)),
                ('experience', models.CharField(max_length=100, null=True)),
                ('education', models.CharField(max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorAssistantMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assistant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Assistant')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorScheduleMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalProcedure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('addInfo', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('type', models.CharField(max_length=1000)),
                ('genericName', models.CharField(max_length=1000)),
                ('manufacturer', models.CharField(max_length=1000)),
                ('addInfo', models.CharField(max_length=1000)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nationalId', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('bloodGroup', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], default='A+', max_length=5)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='M', max_length=10)),
                ('dob', models.DateField(help_text='YYYY-MM-DD', null=True)),
                ('userType', models.CharField(choices=[('D', 'Doctor'), ('P', 'Patient'), ('A', 'Assitant'), ('T', 'Technician')], default='P', max_length=10)),
                ('additionalDetails', models.CharField(max_length=100)),
                ('ratSum', models.FloatField(default=0)),
                ('ratCnt', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateBecamePatient', models.DateField(help_text='YYYY-MM-DD', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrescribedMedicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addInfo', models.CharField(max_length=100)),
                ('amount', models.IntegerField(default=0)),
                ('medicine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Medicine')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptoms', models.CharField(max_length=100, null=True)),
                ('diseases', models.CharField(max_length=100, null=True)),
                ('addInfo', models.CharField(max_length=100, null=True)),
                ('appointment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Appointment')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(default='0', max_length=100, null=True)),
                ('addInfo', models.CharField(max_length=100, null=True)),
                ('token', models.CharField(default='<built-in function id>', max_length=100, unique=True)),
                ('file', models.FileField(null=True, upload_to='reports')),
                ('status', models.CharField(choices=[('U', 'Uploaded'), ('P', 'Pending')], default='P', max_length=10)),
                ('procedure', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.MedicalProcedure')),
                ('record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Record')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('text', models.CharField(max_length=100)),
                ('recipient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('road', models.CharField(max_length=100, null=True)),
                ('day', models.CharField(choices=[('Saturday', 'Saturday'), ('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], max_length=10, null=True)),
                ('startTime', models.TimeField(null=True)),
                ('endTime', models.TimeField(null=True)),
                ('zone', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.CityAreaMapping')),
            ],
        ),
        migrations.CreateModel(
            name='Technician',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='prescribedmedicine',
            name='record',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Record'),
        ),
        migrations.AddField(
            model_name='doctorschedulemapping',
            name='schedule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Schedule'),
        ),
        migrations.AddField(
            model_name='assistantshiprequest',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Doctor'),
        ),
        migrations.AddField(
            model_name='appointmentrequest',
            name='dsm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.DoctorScheduleMapping'),
        ),
        migrations.AddField(
            model_name='appointmentrequest',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Patient'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='assistant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Assistant'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='dsm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.DoctorScheduleMapping'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Patient'),
        ),
        migrations.AddField(
            model_name='access',
            name='record',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Record'),
        ),
        migrations.AlterUniqueTogether(
            name='assistantshiprequest',
            unique_together=set([('doctor', 'assistant')]),
        ),
        migrations.AlterUniqueTogether(
            name='appointmentrequest',
            unique_together=set([('patient', 'dsm', 'dateOfApp')]),
        ),
    ]
