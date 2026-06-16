from rest_framework import serializers
from .models import (
    IMC1Record, IMC2Record, SysmacRecord, DQRecord,
    PlanetMaster, PlanetClient,
    IMC1RecordLedgers, IMC2RecordLedgers, PlanetLedgers,
    SysmacRecordLedgers, DQRecordsLedgers,
    PlanetInvMast, IMC1InvMast, IMC2InvMast, SysmacInvMast, DQInvMast,
    AccMaster, AccProduct,
)
import logging
from decimal import Decimal, InvalidOperation
from datetime import datetime
import json

logger = logging.getLogger(__name__)


# ── Base serializers ──────────────────────────────────────────────────────────

class BaseLedgerSerializer(serializers.ModelSerializer):
    """Base serializer for all ledger models with common field handling"""

    def to_internal_value(self, data):
        if 'entry_date' in data and data['entry_date']:
            try:
                if isinstance(data['entry_date'], str):
                    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']:
                        try:
                            parsed_date = datetime.strptime(data['entry_date'], fmt).date()
                            data['entry_date'] = parsed_date.strftime('%Y-%m-%d')
                            break
                        except ValueError:
                            continue
                    else:
                        logger.warning(f"Could not parse date: {data['entry_date']}")
                        data['entry_date'] = None
            except Exception as e:
                logger.warning(f"Date parsing error: {e}")
                data['entry_date'] = None

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

        for field in ['code', 'particulars', 'entry_mode', 'narration']:
            if field in data and data[field] is None:
                data[field] = ''

        return super().to_internal_value(data)


# ── IMC1 — managed=True, has auto id ─────────────────────────────────────────

class IMC1Serializer(serializers.ModelSerializer):
    opening_balance   = serializers.FloatField(allow_null=True, default=0.0)
    debit             = serializers.FloatField(allow_null=True, default=0.0)
    credit            = serializers.FloatField(allow_null=True, default=0.0)
    place             = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    phone2            = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    openingdepartment = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    balance           = serializers.SerializerMethodField()

    class Meta:
        model  = IMC1Record
        fields = ['id', 'code', 'name', 'opening_balance', 'debit', 'credit',
                  'place', 'phone2', 'openingdepartment', 'synced_at', 'balance']

    def get_balance(self, obj):
        return (obj.debit or 0) - (obj.credit or 0)

    def to_internal_value(self, data):
        data = data.copy()
        if data.get('opening_balance') is None: data['opening_balance'] = 0.0
        if data.get('debit') is None:           data['debit'] = 0.0
        if data.get('credit') is None:          data['credit'] = 0.0
        for f in ('place', 'phone2', 'openingdepartment'):
            if data.get(f) is None: data[f] = ''
        return super().to_internal_value(data)


class IMC1LedgersSerializer(BaseLedgerSerializer):
    entry_date  = serializers.DateField(required=False, allow_null=True)
    debit       = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    credit      = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    voucher_no  = serializers.DecimalField(max_digits=12, decimal_places=0, required=False, allow_null=True)
    code        = serializers.CharField(max_length=30, required=True)
    particulars = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    entry_mode  = serializers.CharField(max_length=30,  required=False, allow_null=True, allow_blank=True)
    narration   = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model  = IMC1RecordLedgers
        fields = '__all__'


# ── IMC2 — managed=True, has auto id ─────────────────────────────────────────

class IMC2Serializer(serializers.ModelSerializer):
    opening_balance   = serializers.FloatField(allow_null=True, default=0.0)
    debit             = serializers.FloatField(allow_null=True, default=0.0)
    credit            = serializers.FloatField(allow_null=True, default=0.0)
    place             = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    phone2            = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    openingdepartment = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    balance           = serializers.SerializerMethodField()

    class Meta:
        model  = IMC2Record
        fields = ['id', 'code', 'name', 'opening_balance', 'debit', 'credit',
                  'place', 'phone2', 'openingdepartment', 'synced_at', 'balance']

    def get_balance(self, obj):
        return (obj.debit or 0) - (obj.credit or 0)

    def to_internal_value(self, data):
        data = data.copy()
        if data.get('opening_balance') is None: data['opening_balance'] = 0.0
        if data.get('debit') is None:           data['debit'] = 0.0
        if data.get('credit') is None:          data['credit'] = 0.0
        for f in ('place', 'phone2', 'openingdepartment'):
            if data.get(f) is None: data[f] = ''
        return super().to_internal_value(data)


class IMC2LedgersSerializer(BaseLedgerSerializer):
    entry_date  = serializers.DateField(required=False, allow_null=True)
    debit       = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    credit      = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    voucher_no  = serializers.DecimalField(max_digits=12, decimal_places=0, required=False, allow_null=True)
    code        = serializers.CharField(max_length=30, required=True)
    particulars = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    entry_mode  = serializers.CharField(max_length=30,  required=False, allow_null=True, allow_blank=True)
    narration   = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model  = IMC2RecordLedgers
        fields = '__all__'


# ── Sysmac — managed=True, has auto id ───────────────────────────────────────

class SysmacSerializer(serializers.ModelSerializer):
    opening_balance   = serializers.FloatField(allow_null=True, default=0.0)
    debit             = serializers.FloatField(allow_null=True, default=0.0)
    credit            = serializers.FloatField(allow_null=True, default=0.0)
    place             = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    phone2            = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    openingdepartment = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    balance           = serializers.SerializerMethodField()

    class Meta:
        model  = SysmacRecord
        fields = ['id', 'code', 'name', 'opening_balance', 'debit', 'credit',
                  'place', 'phone2', 'openingdepartment', 'synced_at', 'balance']

    def get_balance(self, obj):
        return (obj.debit or 0) - (obj.credit or 0)

    def to_internal_value(self, data):
        data = data.copy()
        if data.get('opening_balance') is None: data['opening_balance'] = 0.0
        if data.get('debit') is None:           data['debit'] = 0.0
        if data.get('credit') is None:          data['credit'] = 0.0
        for f in ('place', 'phone2', 'openingdepartment'):
            if data.get(f) is None: data[f] = ''
        return super().to_internal_value(data)


class SysmacLedgersSerializer(BaseLedgerSerializer):
    entry_date  = serializers.DateField(required=False, allow_null=True)
    debit       = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    credit      = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    voucher_no  = serializers.DecimalField(max_digits=12, decimal_places=0, required=False, allow_null=True)
    code        = serializers.CharField(max_length=30, required=True)
    particulars = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    entry_mode  = serializers.CharField(max_length=30,  required=False, allow_null=True, allow_blank=True)
    narration   = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model  = SysmacRecordLedgers
        fields = '__all__'


# ── DQ — managed=True, has auto id ───────────────────────────────────────────

class DQSerializer(serializers.ModelSerializer):
    opening_balance   = serializers.FloatField(allow_null=True, default=0.0)
    debit             = serializers.FloatField(allow_null=True, default=0.0)
    credit            = serializers.FloatField(allow_null=True, default=0.0)
    place             = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    phone2            = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    openingdepartment = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    balance           = serializers.SerializerMethodField()

    class Meta:
        model  = DQRecord
        fields = ['id', 'code', 'name', 'opening_balance', 'debit', 'credit',
                  'place', 'phone2', 'openingdepartment', 'synced_at', 'balance']

    def get_balance(self, obj):
        return (obj.debit or 0) - (obj.credit or 0)

    def to_internal_value(self, data):
        data = data.copy()
        if data.get('opening_balance') is None: data['opening_balance'] = 0.0
        if data.get('debit') is None:           data['debit'] = 0.0
        if data.get('credit') is None:          data['credit'] = 0.0
        for f in ('place', 'phone2', 'openingdepartment'):
            if data.get(f) is None: data[f] = ''
        return super().to_internal_value(data)


class DQLedgersSerializer(BaseLedgerSerializer):
    entry_date  = serializers.DateField(required=False, allow_null=True)
    debit       = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    credit      = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    voucher_no  = serializers.DecimalField(max_digits=12, decimal_places=0, required=False, allow_null=True)
    code        = serializers.CharField(max_length=30, required=True)
    particulars = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    entry_mode  = serializers.CharField(max_length=30,  required=False, allow_null=True, allow_blank=True)
    narration   = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model  = DQRecordsLedgers
        fields = '__all__'


# ── Planet Master — managed=False, NO auto id ─────────────────────────────────

class PlanetMasterSerializer(serializers.ModelSerializer):
    opening_balance   = serializers.FloatField(allow_null=True, default=0.0)
    debit             = serializers.FloatField(allow_null=True, default=0.0)
    credit            = serializers.FloatField(allow_null=True, default=0.0)
    place             = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    phone2            = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    openingdepartment = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    balance           = serializers.SerializerMethodField()

    class Meta:
        model  = PlanetMaster
        # managed=False → no auto id column in the DB
        fields = ['code', 'name', 'super_code', 'opening_balance', 'debit', 'credit',
                  'place', 'phone2', 'openingdepartment', 'balance']

    def get_balance(self, obj):
        return (obj.debit or 0) - (obj.credit or 0)

    def to_internal_value(self, data):
        data = data.copy()
        if data.get('opening_balance') is None: data['opening_balance'] = 0.0
        if data.get('debit') is None:           data['debit'] = 0.0
        if data.get('credit') is None:          data['credit'] = 0.0
        for f in ('place', 'phone2', 'openingdepartment'):
            if data.get(f) is None: data[f] = ''
        return super().to_internal_value(data)


# ── Planet Ledgers — managed=False, pk=code ──────────────────────────────────

class PlanetLedgersSerializer(BaseLedgerSerializer):
    entry_date  = serializers.DateField(required=False, allow_null=True)
    debit       = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    credit      = serializers.DecimalField(max_digits=15, decimal_places=5, required=False, allow_null=True)
    voucher_no  = serializers.DecimalField(max_digits=12, decimal_places=0, required=False, allow_null=True)
    code        = serializers.CharField(max_length=30, required=True)
    particulars = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    entry_mode  = serializers.CharField(max_length=30,  required=False, allow_null=True, allow_blank=True)
    narration   = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model  = PlanetLedgers
        fields = '__all__'


# ── Planet Clients — managed=False, pk=code, NO auto id ──────────────────────

class PlanetClientsSerializer(serializers.ModelSerializer):
    """
    PlanetClient is managed=False — no auto id column.
    Label SerializerMethodFields are read-only (GET only); excluded from
    validated_data so bulk_create never receives them as model kwargs.
    """
    code             = serializers.CharField(required=True, allow_null=False, allow_blank=False)  # FIX: PK — must be present
    name             = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    address          = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    branch           = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    district         = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    state            = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    software         = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    mobile           = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    installationdate = serializers.DateField(
        required=False, allow_null=True,
        input_formats=['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', 'iso-8601'],
    )
    priorty          = serializers.IntegerField(required=False, allow_null=True)
    directdealing    = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    rout             = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    amc              = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    amcamt           = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    accountcode      = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    address3         = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    lictype          = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    clients          = serializers.IntegerField(required=False, allow_null=True)
    sp               = serializers.IntegerField(required=False, allow_null=True)
    nature           = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    # Read-only display labels — present on GET, ignored on POST
    directdealing_label = serializers.SerializerMethodField()
    amc_label           = serializers.SerializerMethodField()
    lictype_label       = serializers.SerializerMethodField()

    client_id = serializers.CharField(max_length=50, required=False, allow_blank=True, default='')

    class Meta:
        model  = PlanetClient
        # No 'id' — managed=False. Label fields listed but marked read_only.
        fields = [
            'code', 'name', 'address', 'branch', 'district', 'state',
            'software', 'mobile', 'installationdate', 'priorty',
            'directdealing', 'directdealing_label',
            'rout', 'amc', 'amc_label', 'amcamt', 'accountcode',
            'address3', 'lictype', 'lictype_label', 'clients', 'sp', 'nature',
            'client_id',
        ]
        read_only_fields = ['directdealing_label', 'amc_label', 'lictype_label']

    def get_directdealing_label(self, obj):
        return {'Y': 'Yes', 'S': 'Self', 'N': 'Dealing No'}.get(obj.directdealing, 'Unknown')

    def get_amc_label(self, obj):
        return {'F': 'Free', 'A': 'SUC', 'S': 'Service Charge'}.get(obj.amc, 'Unknown')

    def get_lictype_label(self, obj):
        return {'E': 'Enterprise', 'P': 'Professional'}.get(obj.lictype, 'Unknown')


# ── InvMast base — all managed=True, have auto id ────────────────────────────

class BaseInvMastSerializer(serializers.ModelSerializer):
    modeofpayment = serializers.CharField(max_length=1,  allow_null=True, allow_blank=True, required=False)
    customerid    = serializers.CharField(max_length=50, allow_null=True, allow_blank=True, required=False)
    invdate       = serializers.DateField(allow_null=True, required=False)
    nettotal      = serializers.DecimalField(max_digits=12, decimal_places=3, allow_null=True, required=False)
    paid          = serializers.DecimalField(max_digits=12, decimal_places=3, allow_null=True, required=False)
    bill_ref      = serializers.CharField(max_length=20, allow_null=True, allow_blank=True, required=False)

    def to_internal_value(self, data):
        if 'invdate' in data and data['invdate']:
            try:
                if isinstance(data['invdate'], str):
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

        for field in ['modeofpayment', 'customerid', 'bill_ref']:
            if field in data and data[field] is None:
                data[field] = ''

        return super().to_internal_value(data)


class PlanetInvMastSerializer(BaseInvMastSerializer):
    class Meta:
        model  = PlanetInvMast
        fields = '__all__'

class IMC1InvMastSerializer(BaseInvMastSerializer):
    class Meta:
        model  = IMC1InvMast
        fields = '__all__'

class IMC2InvMastSerializer(BaseInvMastSerializer):
    class Meta:
        model  = IMC2InvMast
        fields = '__all__'

class SysmacInvMastSerializer(BaseInvMastSerializer):
    class Meta:
        model  = SysmacInvMast
        fields = '__all__'

class DQInvMastSerializer(BaseInvMastSerializer):
    class Meta:
        model  = DQInvMast
        fields = '__all__'


# ── AccMaster — managed=False, NO auto id ────────────────────────────────────

class AccMasterSerializer(serializers.ModelSerializer):
    code              = serializers.CharField(max_length=30)          # FIX: required (it's the PK)
    name              = serializers.CharField(max_length=250)
    super_code        = serializers.CharField(max_length=5,  required=False, allow_null=True, allow_blank=True)
    opening_balance   = serializers.DecimalField(max_digits=12, decimal_places=3, required=False, allow_null=True)
    debit             = serializers.DecimalField(max_digits=16, decimal_places=3, required=False, allow_null=True)
    credit            = serializers.DecimalField(max_digits=16, decimal_places=3, required=False, allow_null=True)
    place             = serializers.CharField(max_length=60, required=False, allow_null=True, allow_blank=True)
    phone2            = serializers.CharField(max_length=60, required=False, allow_null=True, allow_blank=True)
    openingdepartment = serializers.CharField(max_length=30, required=False, allow_null=True, allow_blank=True)
    client_id         = serializers.CharField(max_length=50, required=False, allow_blank=True, default='')

    class Meta:
        model  = AccMaster
        # managed=False → no auto id column, no synced_at column
        fields = ['code', 'name', 'super_code',
                  'opening_balance', 'debit', 'credit',
                  'place', 'phone2', 'openingdepartment', 'client_id']

    def to_internal_value(self, data):
        data = data.copy()
        for field in ('opening_balance', 'debit', 'credit'):
            val = data.get(field)
            if val is None or val == '':
                data[field] = None
            else:
                try:
                    data[field] = str(Decimal(str(val)))
                except (ValueError, InvalidOperation):
                    logger.warning(f"AccMaster: cannot convert {field}={val!r} to Decimal")
                    data[field] = None
        for field in ('super_code', 'place', 'phone2', 'openingdepartment'):
            if data.get(field) is None:
                data[field] = ''
        return super().to_internal_value(data)


# ── AccProduct — managed=False, NO auto id ────────────────────────────────────

class AccProductSerializer(serializers.ModelSerializer):
    code     = serializers.CharField(max_length=30)
    name     = serializers.CharField(max_length=200, required=False, allow_null=True, allow_blank=True)
    catagory = serializers.CharField(max_length=20,  required=False, allow_null=True, allow_blank=True)
    unit     = serializers.CharField(max_length=10,  required=False, allow_null=True, allow_blank=True)
    taxcode  = serializers.CharField(max_length=5,   required=False, allow_null=True, allow_blank=True)
    company  = serializers.CharField(max_length=30,  required=False, allow_null=True, allow_blank=True)
    product  = serializers.CharField(max_length=30,  required=False, allow_null=True, allow_blank=True)
    brand    = serializers.CharField(max_length=30,  required=False, allow_null=True, allow_blank=True)
    text6     = serializers.CharField(max_length=40,  required=False, allow_null=True, allow_blank=True)
    client_id = serializers.CharField(max_length=50, required=False, allow_blank=True, default='')

    class Meta:
        model  = AccProduct
        # managed=False → no auto id column
        fields = ['code', 'name', 'catagory', 'unit', 'taxcode',
                  'company', 'product', 'brand', 'text6', 'client_id']

    def to_internal_value(self, data):
        data = data.copy()
        for field in ('name', 'catagory', 'unit', 'taxcode',
                      'company', 'product', 'brand', 'text6'):
            if data.get(field) is None:
                data[field] = ''
        return super().to_internal_value(data)
from .models import AccDepartment

class AccDepartmentSerializer(serializers.ModelSerializer):
    department_id = serializers.CharField(max_length=30)
    department    = serializers.CharField(max_length=100)
    client_id     = serializers.CharField(max_length=50, required=False, allow_blank=True, default='')

    class Meta:
        model  = AccDepartment
        fields = ['department_id', 'department', 'client_id']
