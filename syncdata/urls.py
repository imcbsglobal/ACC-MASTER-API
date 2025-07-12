from django.urls import path
from .views import IMC1RecordView, IMC2RecordView, SysmacRecordView, DQRecordView, PlanetClientsRecordView, PlanetMasterRecordView

urlpatterns = [
    # SYNC - API'S
    path('imc1/', IMC1RecordView.as_view()),
    path('imc2/', IMC2RecordView.as_view()),
    path('sysmac-info/', SysmacRecordView.as_view()),
    path('dq/', DQRecordView.as_view()),
    path('rrc-clients/', PlanetClientsRecordView.as_view()),
    path('sysmac/', PlanetMasterRecordView.as_view()),
]
