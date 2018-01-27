from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^uninstall_webhook_callback/', views.uninstall_webhook_callback, name='uninstall_webhook_callback'),
    url(r'^help/', views.help, name='help'),
    url(r'^settime/', views.setTime, name='saveTime'),
    url(r'^saveconf/', views.saveConf, name='saveConf'),
    url(r'^get_settings/', views.get_settings, name='get_settings'),
]