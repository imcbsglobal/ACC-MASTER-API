from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import IMC1Record, IMC2Record, SysmacRecord, DQRecord, PlanetMaster, PlanetClient
from .serializers import IMC1Serializer, IMC2Serializer, SysmacSerializer, DQSerializer, PlanetClientsSerializer, PlanetMasterSerializer
import logging
import json
import traceback

logger = logging.getLogger(__name__)

class IMC1RecordView(APIView):
    def post(self, request):
        logger.info(f"IMC1 - Received {len(request.data)} records")
        serializer = IMC1Serializer(data=request.data, many=True)
        if serializer.is_valid():
            with transaction.atomic(): 
                IMC1Record.objects.all().delete()
                records = [IMC1Record(**item) for item in serializer.validated_data]
                IMC1Record.objects.bulk_create(records, batch_size=1000)
            logger.info(f"Saved {len(records)} IMC-1 records")
            return Response({"message": "IMC-1 records saved"}, status=status.HTTP_201_CREATED)
        
        # Enhanced error logging
        logger.error(f"IMC1 Validation Errors: {json.dumps(serializer.errors, indent=2)}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        records = IMC1Record.objects.all()
        serializer = IMC1Serializer(records, many=True)
        return Response(serializer.data)

class IMC2RecordView(APIView):
    def post(self, request):
        logger.info(f"IMC2 - Received {len(request.data)} records")
        serializer = IMC2Serializer(data=request.data, many=True)
        if serializer.is_valid():
            with transaction.atomic():
                IMC2Record.objects.all().delete()
                records = [IMC2Record(**item) for item in serializer.validated_data]
                IMC2Record.objects.bulk_create(records, batch_size=1000)
            logger.info(f"Saved {len(records)} IMC-2 records")
            return Response({"message": "IMC-2 records saved"}, status=status.HTTP_201_CREATED)
        
        # Enhanced error logging
        logger.error(f"IMC2 Validation Errors: {json.dumps(serializer.errors, indent=2)}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        records = IMC2Record.objects.all()
        serializer = IMC2Serializer(records, many=True)
        return Response(serializer.data)

class SysmacRecordView(APIView):
    def post(self, request):
        logger.info(f"Sysmac - Received {len(request.data)} records")
        
        # Log sample data to debug
        if request.data:
            logger.info(f"Sysmac - Sample record: {json.dumps(request.data[0], indent=2)}")
        
        serializer = SysmacSerializer(data=request.data, many=True)
        if serializer.is_valid():
            with transaction.atomic():
                SysmacRecord.objects.all().delete()
                records = [SysmacRecord(**item) for item in serializer.validated_data]
                SysmacRecord.objects.bulk_create(records, batch_size=1000)
            logger.info(f"Saved {len(records)} Sysmac records")
            return Response({"message": "Sysmac records saved"}, status=status.HTTP_201_CREATED)
        
        # Enhanced error logging
        logger.error(f"Sysmac Validation Errors: {json.dumps(serializer.errors, indent=2)}")
        
        # Log the first few invalid records for debugging
        if hasattr(serializer, 'initial_data') and serializer.initial_data:
            for i, record in enumerate(serializer.initial_data[:3]):  # First 3 records
                logger.error(f"Sysmac - Invalid record {i}: {json.dumps(record, indent=2)}")
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        records = SysmacRecord.objects.all()
        serializer = SysmacSerializer(records, many=True)
        return Response(serializer.data)

class DQRecordView(APIView):
    def post(self, request):
        logger.info(f"DQ - Received {len(request.data)} records")
        
        # Log sample data to debug
        if request.data:
            logger.info(f"DQ - Sample record: {json.dumps(request.data[0], indent=2)}")
        
        serializer = DQSerializer(data=request.data, many=True)
        if serializer.is_valid():
            with transaction.atomic():
                DQRecord.objects.all().delete()
                records = [DQRecord(**item) for item in serializer.validated_data]
                DQRecord.objects.bulk_create(records, batch_size=1000)
            logger.info(f"Saved {len(records)} DQ records")
            return Response({"message": "DQ records saved"}, status=status.HTTP_201_CREATED)
        
        # Enhanced error logging
        logger.error(f"DQ Validation Errors: {json.dumps(serializer.errors, indent=2)}")
        
        # Log the first few invalid records for debugging
        if hasattr(serializer, 'initial_data') and serializer.initial_data:
            for i, record in enumerate(serializer.initial_data[:3]):  # First 3 records
                logger.error(f"DQ - Invalid record {i}: {json.dumps(record, indent=2)}")
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        records = DQRecord.objects.all()
        serializer = DQSerializer(records, many=True)
        return Response(serializer.data)
    

class PlanetMasterRecordView(APIView):
    def post(self, request):
        try:
            logger.info(f"PLANET_MASTER - Received {len(request.data)} records")
            serializer = PlanetMasterSerializer(data=request.data, many=True)
            if serializer.is_valid():
                with transaction.atomic():
                    PlanetMaster.objects.all().delete()
                    records = [PlanetMaster(**item) for item in serializer.validated_data]
                    PlanetMaster.objects.bulk_create(records, batch_size=1000)
                logger.info(f"Saved {len(records)} PLANET_MASTER records")
                return Response({"message": "PLANET_MASTER records saved"}, status=status.HTTP_201_CREATED)

            logger.error(f"PLANET_MASTER Validation Errors: {json.dumps(serializer.errors, indent=2)}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"PLANET_MASTER Exception: {str(e)}")
            logger.error(traceback.format_exc())
            if request.data:
                logger.error(f"Sample record: {json.dumps(request.data[0], indent=2)}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        records = PlanetMaster.objects.all()
        serializer = PlanetMasterSerializer(records, many=True)
        return Response(serializer.data)



class PlanetClientsRecordView(APIView):
    def post(self, request):
        try:
            logger.info(f"PLANET_CLIENTS - Received {len(request.data)} records")
            
            # Log first few records to see data structure
            for i, record in enumerate(request.data[:2]):
                logger.info(f"Sample record {i}: {json.dumps(record, indent=2, default=str)}")
            
            serializer = PlanetClientsSerializer(data=request.data, many=True)
            if serializer.is_valid():
                with transaction.atomic():
                    PlanetClient.objects.all().delete()
                    records = [PlanetClient(**item) for item in serializer.validated_data]
                    PlanetClient.objects.bulk_create(records, batch_size=1000)
                logger.info(f"Saved {len(records)} PLANET_CLIENTS records")
                return Response({"message": "PLANET_CLIENTS records saved"}, status=status.HTTP_201_CREATED)

            # ENHANCED ERROR LOGGING - This will show you exactly what's wrong
            logger.error(f"Validation failed for PLANET_CLIENTS")
            logger.error(f"Total errors: {len(serializer.errors)}")
            
            error_count = 0
            for idx, err in enumerate(serializer.errors):
                if err:  # Only log records with actual errors
                    error_count += 1
                    logger.error(f"Record {idx} has validation errors:")
                    logger.error(f"   Errors: {json.dumps(err, indent=4)}")
                    
                    # Show the actual problematic record
                    if idx < len(request.data):
                        logger.error(f"   Record data: {json.dumps(request.data[idx], indent=4, default=str)}")
                    
                    # Stop after first 5 errors to avoid log spam
                    if error_count >= 5:
                        logger.error(f"... and {len([e for e in serializer.errors if e])} more records with errors")
                        break
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f" PLANET_CLIENTS Exception: {str(e)}")
            logger.error(traceback.format_exc())
            if request.data:
                logger.error(f"Sample record: {json.dumps(request.data[0], indent=2, default=str)}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        records = PlanetClient.objects.all()
        serializer = PlanetClientsSerializer(records, many=True)
        return Response(serializer.data)