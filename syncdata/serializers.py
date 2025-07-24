from rest_framework import serializers
from .models import IMC1Record, IMC2Record, SysmacRecord, DQRecord, PlanetMaster, PlanetClient, IMC1RecordLedgers, IMC2RecordLedgers, PlanetLedgers, SysmacRecordLedgers, DQRecordsLedgers, PlanetInvMast, IMC1InvMast, IMC2InvMast, SysmacInvMast, DQInvMast
import logging
from decimal import Decimal, InvalidOperation
from datetime import datetime
import json

# Get logger
logger = logging.getLogger(__name__)

class BaseLedgerSerializer(serializers.ModelSerializer):
    """Base serializer for all ledger models with common field handling"""
    
    def to_internal_value(self, data):
        # Handle date field conversion
        if 'entry_date' in data and data['entry_date']:
            try:
                if isinstance(data['entry_date'], str):
                    # Try different date formats
                    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']:
                        try:
                            parsed_date = datetime.strptime(data['entry_date'], fmt).date()
                            data['entry_date'] = parsed_date.strftime('%Y-%m-%d')
                            break
                        except ValueError:
                            continue
                    else:
                        # If none of the formats work, set to None
                        logger.warning(f"Could not parse date: {data['entry_date']}")
                        data['entry_date'] = None
            except Exception as e:
                logger.warning(f"Date parsing error: {e}")
                data['entry_date'] = None
        
        # Handle decimal fields
        for field in ['debit', 'credit', 'voucher_no']:
            if field in data and data[field] is not None:
                try:
                    if isinstance(data[field], str) and data[field].strip() == '':
                        data[field] = None
                    elif data[field] is not None:
                        data[field] = Decimal(str(data[field]))
                except (ValueError, InvalidOperation):
                    logger.warning(f"Could not convert {field} to decimal: {data[field]}")
                    data[field] = None
        
        # Handle string fields - convert None to empty string
        for field in ['code', 'particulars', 'entry_mode', 'narration']:
            if field in data and data[field] is None:
                data[field] = ''
        
        return super().to_internal_value(data)

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

class IMC1LedgersSerializer(BaseLedgerSerializer):
    entry_date = serializers.DateField(required=False, allow_null=True)
    debit = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    credit = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    voucher_no = serializers.DecimalField(max_digits=12, decimal_places=0, required=False, allow_null=True)
    code = serializers.CharField(max_length=30, required=True)
    particulars = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    entry_mode = serializers.CharField(max_length=30, required=False, allow_null=True, allow_blank=True)
    narration = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model = IMC1RecordLedgers
        fields = '__all__'

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

class IMC2LedgersSerializer(BaseLedgerSerializer):
    entry_date = serializers.DateField(required=False, allow_null=True)
    debit = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    credit = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    voucher_no = serializers.DecimalField(max_digits=12, decimal_places=0, required=False, allow_null=True)
    code = serializers.CharField(max_length=30, required=True)
    particulars = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    entry_mode = serializers.CharField(max_length=30, required=False, allow_null=True, allow_blank=True)
    narration = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model = IMC2RecordLedgers
        fields = '__all__'

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
    
class SysmacLedgersSerializer(BaseLedgerSerializer):
    entry_date = serializers.DateField(required=False, allow_null=True)
    debit = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    credit = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    voucher_no = serializers.DecimalField(max_digits=12, decimal_places=0, required=False, allow_null=True)
    code = serializers.CharField(max_length=30, required=True)
    particulars = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    entry_mode = serializers.CharField(max_length=30, required=False, allow_null=True, allow_blank=True)
    narration = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model = SysmacRecordLedgers
        fields = '__all__'


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
    

class DQLedgersSerializer(BaseLedgerSerializer):
    entry_date = serializers.DateField(required=False, allow_null=True)
    debit = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    credit = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    voucher_no = serializers.DecimalField(max_digits=12, decimal_places=0, required=False, allow_null=True)
    code = serializers.CharField(max_length=30, required=True)
    particulars = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    entry_mode = serializers.CharField(max_length=30, required=False, allow_null=True, allow_blank=True)
    narration = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model = DQRecordsLedgers
        fields = '__all__'

    
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
    

class PlanetLedgersSerializer(BaseLedgerSerializer):
    entry_date = serializers.DateField(required=False, allow_null=True)
    debit = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    credit = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    voucher_no = serializers.DecimalField(max_digits=12, decimal_places=0, required=False, allow_null=True)
    code = serializers.CharField(max_length=30, required=True)
    particulars = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    entry_mode = serializers.CharField(max_length=30, required=False, allow_null=True, allow_blank=True)
    narration = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model = PlanetLedgers
        fields = '__all__'

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



class BaseInvMastSerializer(serializers.ModelSerializer):
    """Base serializer for all invoice master models with common field handling"""
    
    modeofpayment = serializers.CharField(max_length=1, allow_null=True, allow_blank=True, required=False)
    customerid = serializers.CharField(max_length=50, allow_null=True, allow_blank=True, required=False)  # Increased from 5 to 50
    invdate = serializers.DateField(allow_null=True, required=False)
    nettotal = serializers.DecimalField(max_digits=12, decimal_places=3, allow_null=True, required=False)
    paid = serializers.DecimalField(max_digits=12, decimal_places=3, allow_null=True, required=False)
    bill_ref = serializers.CharField(max_length=20, allow_null=True, allow_blank=True, required=False)
    
    def to_internal_value(self, data):
        # Handle date field conversion
        if 'invdate' in data and data['invdate']:
            try:
                if isinstance(data['invdate'], str):
                    # Try different date formats
                    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']:
                        try:
                            parsed_date = datetime.strptime(data['invdate'], fmt).date()
                            data['invdate'] = parsed_date.strftime('%Y-%m-%d')
                            break
                        except ValueError:
                            continue
                    else:
                        logger.warning(f"Could not parse invdate: {data['invdate']}")
                        data['invdate'] = None
            except Exception as e:
                logger.warning(f"InvDate parsing error: {e}")
                data['invdate'] = None
        
        # Handle decimal fields
        for field in ['nettotal', 'paid']:
            if field in data and data[field] is not None:
                try:
                    if isinstance(data[field], str) and data[field].strip() == '':
                        data[field] = None
                    elif data[field] is not None:
                        data[field] = Decimal(str(data[field]))
                except (ValueError, InvalidOperation):
                    logger.warning(f"Could not convert {field} to decimal: {data[field]}")
                    data[field] = None
        
        # Handle string fields - convert None to empty string
        for field in ['modeofpayment', 'customerid', 'bill_ref']:
            if field in data and data[field] is None:
                data[field] = ''
        
        return super().to_internal_value(data)

class PlanetInvMastSerializer(BaseInvMastSerializer):
    class Meta:
        model = PlanetInvMast
        fields = '__all__'

class IMC1InvMastSerializer(BaseInvMastSerializer):
    class Meta:
        model = IMC1InvMast
        fields = '__all__'

class IMC2InvMastSerializer(BaseInvMastSerializer):
    class Meta:
        model = IMC2InvMast
        fields = '__all__'

class SysmacInvMastSerializer(BaseInvMastSerializer):
    class Meta:
        model = SysmacInvMast
        fields = '__all__'

class DQInvMastSerializer(BaseInvMastSerializer):
    class Meta:
        model = DQInvMast
        fields = '__all__'