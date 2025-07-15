from django.urls import path
from .views import IMC1RecordView, IMC1LedgersView, IMC2RecordView,IMC2LedgersView, SysmacRecordView, SysmacLedgersView, DQRecordView,DQLedgersView, PlanetClientsRecordView, PlanetLedgersView, PlanetMasterRecordView

urlpatterns = [
    # SYNC - API'S
    path('imc1/', IMC1RecordView.as_view()),
    path('imc1-ledgers/', IMC1LedgersView.as_view()),
    path('imc2/', IMC2RecordView.as_view()),
    path('imc2-ledgers/', IMC2LedgersView.as_view()),
    path('sysmac-info/', SysmacRecordView.as_view()),
    path('sysmac-info-ledgers/', SysmacLedgersView.as_view()),
    path('dq/', DQRecordView.as_view()),
    path('dq-ledgers/', DQLedgersView.as_view()),
    path('sysmac/', PlanetMasterRecordView.as_view()),
    path('sysmac-ledgers/', PlanetLedgersView.as_view()),
    path('rrc-clients/', PlanetClientsRecordView.as_view()),
]
