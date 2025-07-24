# Update your urls.py file with these additions

from django.urls import path
from .views import (
    IMC1RecordView, IMC1LedgersView, IMC1InvMastView,
    IMC2RecordView, IMC2LedgersView, IMC2InvMastView,
    SysmacRecordView, SysmacLedgersView, SysmacInvMastView,
    DQRecordView, DQLedgersView, DQInvMastView,
    PlanetClientsRecordView, PlanetLedgersView, PlanetMasterRecordView, PlanetInvMastView
)

urlpatterns = [
    # SYNC - API'S
    path('imc1/', IMC1RecordView.as_view()),
    path('imc1-ledgers/', IMC1LedgersView.as_view()),
    path('imc1-invmast/', IMC1InvMastView.as_view()),
    
    path('imc2/', IMC2RecordView.as_view()),
    path('imc2-ledgers/', IMC2LedgersView.as_view()),
    path('imc2-invmast/', IMC2InvMastView.as_view()),
    
    path('sysmac-info/', SysmacRecordView.as_view()),
    path('sysmac-info-ledgers/', SysmacLedgersView.as_view()),
    path('sysmac-info-invmast/', SysmacInvMastView.as_view()),
    
    path('dq/', DQRecordView.as_view()),
    path('dq-ledgers/', DQLedgersView.as_view()),
    path('dq-invmast/', DQInvMastView.as_view()),
    
    path('sysmac/', PlanetMasterRecordView.as_view()),
    path('sysmac-ledgers/', PlanetLedgersView.as_view()),
    path('sysmac-invmast/', PlanetInvMastView.as_view()),
    
    path('rrc-clients/', PlanetClientsRecordView.as_view()),
]