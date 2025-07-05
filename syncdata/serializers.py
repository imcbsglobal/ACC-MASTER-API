from rest_framework import serializers
from .models import IMC1Record, IMC2Record, SysmacRecord, DQRecord


class IMC1Serializer(serializers.ModelSerializer):
    class Meta:
        model = IMC1Record
        fields = '__all__'


class IMC2Serializer(serializers.ModelSerializer):
    class Meta:
        model = IMC2Record
        fields = '__all__'


class SysmacSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysmacRecord
        fields = '__all__'


class DQSerializer(serializers.ModelSerializer):
    class Meta:
        model = DQRecord
        fields = '__all__'
