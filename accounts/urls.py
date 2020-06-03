from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home, name='accounts'),
    
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^register/$', views.register, name='register'),
    
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^login/$', login, {'template_name': 'accounts/login.html'},name='login'),

    url(r'^logout/$', logout, {'template_name': 'accounts/index.html'},name='logout'),


    
    url(r'^dashboard/$', views.view_dashboard, name='view_dashboard'),

    url(r'^add_appointment/$', views.add_appointment, name='add_appointment'),
    url(r'^profile/add_report/$', views.add_report , name = 'add_report'),
    url(r'^create_prescription/$', views.create_prescription, name='create_prescription'),
    url(r'^request_appointment/$', views.request_appointment, name='request_appointment'),
    url(r'^request_assistant/$', views.request_assistant, name='request_assistant'),

    url(r'^accept_appointment/$', views.accept_appointment, name='accept_appointment'),
    url(r'^accept_assistant/$', views.accept_assistant, name='accept_assistant'),

    url(r'^reject_assistant/$', views.reject_assistant, name='reject_assistant'),
    url(r'^reject_appointment/$', views.reject_appointment, name='reject_appointment'),

    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/search/$', views.search, name='search'),

    url(r'^savemsg/$', views.save_message, name='save_message'),
    url(r'^profile/delete_schedule/$', views.delete_schedule, name='delete_schedule'),
    url(r'^profile/add_schedule/$', views.add_schedule, name='add_schedule'),

    url(r'^meena/$', views.meena, name='meena'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
