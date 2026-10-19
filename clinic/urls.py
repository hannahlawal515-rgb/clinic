from django.urls import path

from . import views

app_name = "clinic"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("patients/add/", views.add_patient, name="add_patient"),
    path("patients/<int:entry_id>/<str:action>/", views.update_status, name="update_status"),
    path("call-next/", views.call_next, name="call_next"),
]