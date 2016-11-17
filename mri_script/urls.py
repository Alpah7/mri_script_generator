from django.conf.urls import url

from . import views

app_name = 'mri_script'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'help', views.help, name='help'),
    url(r'contact', views.contact, name='contact'),
]