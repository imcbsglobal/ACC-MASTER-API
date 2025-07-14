from rest_framework import serializers
from .models import IMC1Record, IMC2Record, SysmacRecord, DQRecord, PlanetMaster, PlanetClient
import logging
import json

# Get logger
logger = logging.getLogger(__name__)

class IMC1Serializer(serializers.ModelSerializer):
    # Handle null values explicitly
    opening_balance = serializers.FloatField(allow_null=True, default=0.0)
    debit = serializers.FloatField(allow_null=True, default=0.0)
    credit = serializers.FloatField(allow_null=True, default=0.0)
    place = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    phone2 = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    openingdepartment = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    
    balance = serializers.SerializerMethodField()
    
    class Meta:
        model = IMC1Record
        fields = [
            'id', 'code', 'name', 'opening_balance', 'debit', 'credit',
            'place', 'phone2', 'openingdepartment', 'synced_at', 'balance'
        ]

    def get_balance(self, obj):
        return (obj.debit or 0) - (obj.credit or 0)

    def to_internal_value(self, data):
        # Convert None to appropriate defaults
        if data.get('opening_balance') is None:
            data['opening_balance'] = 0.0
        if data.get('debit') is None:
            data['debit'] = 0.0
        if data.get('credit') is None:
            data['credit'] = 0.0
        if data.get('place') is None:
            data['place'] = ''
        if data.get('phone2') is None:
            data['phone2'] = ''
        if data.get('openingdepartment') is None:
            data['openingdepartment'] = ''
        return super().to_internal_value(data)


class IMC2Serializer(serializers.ModelSerializer):
    # Handle null values explicitly
    opening_balance = serializers.FloatField(allow_null=True, default=0.0)
    debit = serializers.FloatField(allow_null=True, default=0.0)
    credit = serializers.FloatField(allow_null=True, default=0.0)
    place = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    phone2 = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    openingdepartment = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    
    balance = serializers.SerializerMethodField()
    
    class Meta:
        model = IMC2Record
        fields = [
            'id', 'code', 'name', 'opening_balance', 'debit', 'credit',
            'place', 'phone2', 'openingdepartment', 'synced_at', 'balance'
        ]

    def get_balance(self, obj):
        return (obj.debit or 0) - (obj.credit or 0)

    def to_internal_value(self, data):
        # Convert None to appropriate defaults
        if data.get('opening_balance') is None:
            data['opening_balance'] = 0.0
        if data.get('debit') is None:
            data['debit'] = 0.0
        if data.get('credit') is None:
            data['credit'] = 0.0
        if data.get('place') is None:
            data['place'] = ''
        if data.get('phone2') is None:
            data['phone2'] = ''
        if data.get('openingdepartment') is None:
            data['openingdepartment'] = ''
        return super().to_internal_value(data)


class SysmacSerializer(serializers.ModelSerializer):
    # Handle null values explicitly
    opening_balance = serializers.FloatField(allow_null=True, default=0.0)
    debit = serializers.FloatField(allow_null=True, default=0.0)
    credit = serializers.FloatField(allow_null=True, default=0.0)
    place = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    phone2 = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    openingdepartment = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    
    balance = serializers.SerializerMethodField()
    
    class Meta:
        model = SysmacRecord
        fields = [
            'id', 'code', 'name', 'opening_balance', 'debit', 'credit',
            'place', 'phone2', 'openingdepartment', 'synced_at', 'balance'
        ]

    def get_balance(self, obj):
        return (obj.debit or 0) - (obj.credit or 0)

    def to_internal_value(self, data):
        # Convert None to appropriate defaults
        if data.get('opening_balance') is None:
            data['opening_balance'] = 0.0
        if data.get('debit') is None:
            data['debit'] = 0.0
        if data.get('credit') is None:
            data['credit'] = 0.0
        if data.get('place') is None:
            data['place'] = ''
        if data.get('phone2') is None:
            data['phone2'] = ''
        if data.get('openingdepartment') is None:
            data['openingdepartment'] = ''
        return super().to_internal_value(data)


class DQSerializer(serializers.ModelSerializer):
    # Handle null values explicitly
    opening_balance = serializers.FloatField(allow_null=True, default=0.0)
    debit = serializers.FloatField(allow_null=True, default=0.0)
    credit = serializers.FloatField(allow_null=True, default=0.0)
    place = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    phone2 = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    openingdepartment = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    
    balance = serializers.SerializerMethodField()
    
    class Meta:
        model = DQRecord
        fields = [
            'id', 'code', 'name', 'opening_balance', 'debit', 'credit',
            'place', 'phone2', 'openingdepartment', 'synced_at', 'balance'
        ]

    def get_balance(self, obj):
        return (obj.debit or 0) - (obj.credit or 0)

    def to_internal_value(self, data):
        # Convert None to appropriate defaults
        if data.get('opening_balance') is None:
            data['opening_balance'] = 0.0
        if data.get('debit') is None:
            data['debit'] = 0.0
        if data.get('credit') is None:
            data['credit'] = 0.0
        if data.get('place') is None:
            data['place'] = ''
        if data.get('phone2') is None:
            data['phone2'] = ''
        if data.get('openingdepartment') is None:
            data['openingdepartment'] = ''
        return super().to_internal_value(data)
    

class PlanetMasterSerializer(serializers.ModelSerializer):
    # Handle null values explicitly
    opening_balance = serializers.FloatField(allow_null=True, default=0.0)
    debit = serializers.FloatField(allow_null=True, default=0.0)
    credit = serializers.FloatField(allow_null=True, default=0.0)
    place = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    phone2 = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    openingdepartment = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    
    balance = serializers.SerializerMethodField()
    
    class Meta:
        model = PlanetMaster
        fields = [
            'id', 'code', 'name', 'super_code', 'opening_balance', 'debit', 'credit',
            'place', 'phone2', 'openingdepartment', 'balance'
        ]
        # Note: Removed 'synced_at' as it doesn't exist in PlanetMaster model

    def get_balance(self, obj):
        return (obj.debit or 0) - (obj.credit or 0)

    def to_internal_value(self, data):
        # Convert None to appropriate defaults
        if data.get('opening_balance') is None:
            data['opening_balance'] = 0.0
        if data.get('debit') is None:
            data['debit'] = 0.0
        if data.get('credit') is None:
            data['credit'] = 0.0
        if data.get('place') is None:
            data['place'] = ''
        if data.get('phone2') is None:
            data['phone2'] = ''
        if data.get('openingdepartment') is None:
            data['openingdepartment'] = ''
        return super().to_internal_value(data)

class PlanetClientsSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
    required=False, allow_null=True, allow_blank=True)
    name = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    address = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    branch = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    district = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    state = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    software = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    mobile = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    installationdate = serializers.DateField(required=False, allow_null=True, input_formats=["%Y-%m-%d"])
    priorty = serializers.IntegerField(required=False, allow_null=True)
    directdealing = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    directdealing_label = serializers.SerializerMethodField()
    rout = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    amc = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    amc_label = serializers.SerializerMethodField()
    amcamt = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True)
    accountcode = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    address3 = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    lictype = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    lictype_label = serializers.SerializerMethodField()
    clients = serializers.IntegerField(required=False, allow_null=True)
    sp = serializers.IntegerField(required=False, allow_null=True)
    nature = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model = PlanetClient
        fields = '__all__'

    def get_directdealing_label(self, obj):
        mapping = {
            'Y': 'Yes',
            'S': 'Self',
            'N': 'Dealing No'
        }
        return mapping.get(obj.directdealing, 'Unknown')
    
    def get_amc_label(self, obj):
        mapping = {
            'F': 'Free',
            'A': 'SUC',
            'S': 'Service Charge'
        }
        return mapping.get(obj.amc, 'Unknown')
    
    def get_lictype_label(self, obj):
        mapping = {
            'E': 'Enterprise',
            'P': 'Professional'
        }
        return mapping.get(obj.lictype, 'Unknown')
