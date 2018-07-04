from django.conf.urls import url
import views


urlpatterns = [
    url('^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),
    url(r"^login/$", views.login),
]