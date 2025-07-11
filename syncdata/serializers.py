from rest_framework import serializers
from .models import IMC1Record, IMC2Record, SysmacRecord, DQRecord

#serializer


class IMC1Serializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    class Meta:
        model = IMC1Record
        fields = [
            'id', 'code', 'name', 'opening_balance', 'debit', 'credit',
            'place', 'phone2', 'openingdepartment', 'synced_at', 'balance'
        ]

    def get_balance(self, obj):
        return (obj.opening_balance or 0) + (obj.debit or 0) - (obj.credit or 0)


class IMC2Serializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    class Meta:
        model = IMC2Record
        fields = [
            'id', 'code', 'name', 'opening_balance', 'debit', 'credit',
            'place', 'phone2', 'openingdepartment', 'synced_at', 'balance'
        ]

    def get_balance(self, obj):
        return (obj.opening_balance or 0) + (obj.debit or 0) - (obj.credit or 0)

class SysmacSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    class Meta:
        model = SysmacRecord
        fields = [
            'id', 'code', 'name', 'opening_balance', 'debit', 'credit',
            'place', 'phone2', 'openingdepartment', 'synced_at', 'balance'
        ]

    def get_balance(self, obj):
        return (obj.opening_balance or 0) + (obj.debit or 0) - (obj.credit or 0)


class DQSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    class Meta:
        model = DQRecord
        fields = [
            'id', 'code', 'name', 'opening_balance', 'debit', 'credit',
            'place', 'phone2', 'openingdepartment', 'synced_at', 'balance'
        ]

    def get_balance(self, obj):
        return (obj.opening_balance or 0) + (obj.debit or 0) - (obj.credit or 0)
