from django.conf.urls import url
import views


urlpatterns = [
    url('^register/$', views.register),
]