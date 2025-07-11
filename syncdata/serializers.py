from rest_framework import serializers
from .models import IMC1Record, IMC2Record, SysmacRecord, DQRecord

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