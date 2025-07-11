from rest_framework import serializers
from .models import IMC1Record, IMC2Record, SysmacRecord, DQRecord

#serializer


class IMC1Serializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    class Meta:
        model = IMC1Record
        fields = '__all__'

    def get_balance(self, obj):
        return (obj.opening_balance or 0) + (obj.debit or 0) - (obj.credit or 0)


class IMC2Serializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    class Meta:
        model = IMC2Record
        fields = '__all__'

    def get_balance(self, obj):
        return (obj.opening_balance or 0) + (obj.debit or 0) - (obj.credit or 0)

class SysmacSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    class Meta:
        model = SysmacRecord
        fields = '__all__'

    def get_balance(self, obj):
        return (obj.opening_balance or 0) + (obj.debit or 0) - (obj.credit or 0)


class DQSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    class Meta:
        model = DQRecord
        fields = '__all__'

    def get_balance(self, obj):
        return (obj.opening_balance or 0) + (obj.debit or 0) - (obj.credit or 0)
