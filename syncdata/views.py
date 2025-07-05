from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import IMC1Record, IMC2Record, SysmacRecord, DQRecord
from .serializers import IMC1Serializer, IMC2Serializer, SysmacSerializer, DQSerializer
import logging
logger = logging.getLogger(__name__)

class IMC1RecordView(APIView):
    def post(self, request):
        serializer = IMC1Serializer(data=request.data, many=True)
        if serializer.is_valid():
            with transaction.atomic(): 
                IMC1Record.objects.all().delete()
                # Use bulk_create instead of save()
                records = [IMC1Record(**item) for item in serializer.validated_data]
                IMC1Record.objects.bulk_create(records, batch_size=1000)
            logger.info(f"Saved {len(records)} IMC-1 records")
            return Response({"message": "IMC-1 records saved"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        records = IMC1Record.objects.all()
        serializer = IMC1Serializer(records, many=True)
        return Response(serializer.data)

class IMC2RecordView(APIView):
    def post(self, request):
        serializer = IMC2Serializer(data=request.data, many=True)
        if serializer.is_valid():
            with transaction.atomic():  # Add this
                IMC2Record.objects.all().delete()
                # Use bulk_create instead of save()
                records = [IMC2Record(**item) for item in serializer.validated_data]
                IMC2Record.objects.bulk_create(records, batch_size=1000)
            logger.info(f"Saved {len(records)} IMC-2 records")
            return Response({"message": "IMC-2 records saved"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        records = IMC2Record.objects.all()
        serializer = IMC2Serializer(records, many=True)
        return Response(serializer.data)

class SysmacRecordView(APIView):
    def post(self, request):
        serializer = SysmacSerializer(data=request.data, many=True)
        if serializer.is_valid():
            with transaction.atomic():  # Add this
                SysmacRecord.objects.all().delete()
                # Use bulk_create instead of save()
                records = [SysmacRecord(**item) for item in serializer.validated_data]
                SysmacRecord.objects.bulk_create(records, batch_size=1000)
            logger.info(f"Saved {len(records)} Sysmac records")
            return Response({"message": "Sysmac records saved"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        records = SysmacRecord.objects.all()
        serializer = SysmacSerializer(records, many=True)
        return Response(serializer.data)

class DQRecordView(APIView):
    def post(self, request):
        serializer = DQSerializer(data=request.data, many=True)
        if serializer.is_valid():
            with transaction.atomic():  # Add this
                DQRecord.objects.all().delete()
                # Use bulk_create instead of save()
                records = [DQRecord(**item) for item in serializer.validated_data]
                DQRecord.objects.bulk_create(records, batch_size=1000)
            logger.info(f"Saved {len(records)} DQ records")
            return Response({"message": "DQ records saved"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        records = DQRecord.objects.all()
        serializer = DQSerializer(records, many=True)
        return Response(serializer.data)

