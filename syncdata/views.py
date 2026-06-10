from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import IMC1Record, IMC2Record, SysmacRecord, DQRecord, PlanetMaster, PlanetClient, IMC1RecordLedgers, IMC2RecordLedgers, SysmacRecordLedgers, DQRecordsLedgers, PlanetLedgers, PlanetInvMast, IMC1InvMast, IMC2InvMast, SysmacInvMast, DQInvMast , AccMaster, AccProduct
from .serializers import IMC1Serializer, IMC2Serializer, SysmacSerializer, DQSerializer, PlanetClientsSerializer, PlanetMasterSerializer, IMC1LedgersSerializer, IMC2LedgersSerializer, SysmacLedgersSerializer, DQLedgersSerializer, PlanetLedgersSerializer, PlanetInvMastSerializer, IMC1InvMastSerializer, IMC2InvMastSerializer, SysmacInvMastSerializer, DQInvMastSerializer ,AccMasterSerializer, AccProductSerializer
import logging
import json
import traceback
from datetime import datetime
from decimal import Decimal, InvalidOperation

logger = logging.getLogger(__name__)

class BaseLedgersView(APIView):
    """Base class for all ledgers views with common functionality"""
    
    model = None
    serializer_class = None
    record_type = None
    
    def clean_record(self, record):
        """Clean and validate individual record before serialization"""
        cleaned = record.copy()
        
        # Handle date fields
        if 'entry_date' in cleaned:
            if cleaned['entry_date'] is None or cleaned['entry_date'] == '':
                cleaned['entry_date'] = None
            elif isinstance(cleaned['entry_date'], str):
                # Try to parse various date formats
                date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S', '%d-%m-%Y']
                for fmt in date_formats:
                    try:
                        parsed_date = datetime.strptime(cleaned['entry_date'], fmt).date()
                        cleaned['entry_date'] = parsed_date.strftime('%Y-%m-%d')
                        break
                    except ValueError:
                        continue
                else:
                    logger.warning(f"Could not parse date: {cleaned['entry_date']}")
                    cleaned['entry_date'] = None
        
        # Handle decimal fields
        decimal_fields = ['debit', 'credit', 'voucher_no']
        for field in decimal_fields:
            if field in cleaned:
                if cleaned[field] is None or cleaned[field] == '':
                    cleaned[field] = None
                else:
                    try:
                        cleaned[field] = str(Decimal(str(cleaned[field])))
                    except (ValueError, InvalidOperation, TypeError):
                        logger.warning(f"Could not convert {field} to decimal: {cleaned[field]}")
                        cleaned[field] = None
        
        # Handle string fields
        string_fields = ['code', 'particulars', 'entry_mode', 'narration']
        for field in string_fields:
            if field in cleaned:
                if cleaned[field] is None:
                    cleaned[field] = '' if field != 'code' else None  # code is required
                else:
                    cleaned[field] = str(cleaned[field]).strip()
        
        # Validate required fields
        if not cleaned.get('code'):
            return None  # Invalid record without code
        
        return cleaned
    
    def process_in_chunks(self, data, chunk_size=500):
        """Process data in smaller chunks to identify problematic records"""
        total_records = len(data)
        processed_count = 0
        failed_records = []
        
        logger.info(f"{self.record_type} - Processing {total_records} records in chunks of {chunk_size}")
        
        for i in range(0, total_records, chunk_size):
            chunk = data[i:i + chunk_size]
            chunk_num = (i // chunk_size) + 1
            
            logger.info(f"{self.record_type} - Processing chunk {chunk_num} ({len(chunk)} records)")
            
            # Clean each record in the chunk
            cleaned_chunk = []
            for idx, record in enumerate(chunk):
                cleaned_record = self.clean_record(record)
                if cleaned_record is not None:
                    cleaned_chunk.append(cleaned_record)
                else:
                    failed_records.append({
                        'index': i + idx,
                        'record': record,
                        'error': 'Missing required field: code'
                    })
            
            if not cleaned_chunk:
                logger.warning(f"{self.record_type} - Chunk {chunk_num} has no valid records")
                continue
            
            # Try to serialize the chunk
            serializer = self.serializer_class(data=cleaned_chunk, many=True)
            if serializer.is_valid():
                try:
                    # Use raw SQL insert to avoid ORM id lookup on managed=False tables
                    from django.db import connection as _conn
                    fields = [f.column for f in self.model._meta.concrete_fields if not f.primary_key or not f.auto_created]
                    placeholders = ', '.join(['%s'] * len(fields))
                    col_names = ', '.join(fields)
                    sql = f"INSERT INTO {self.model._meta.db_table} ({col_names}) VALUES ({placeholders})"
                    rows = [
                        tuple(item.get(f.attname, None) for f in self.model._meta.concrete_fields if not f.primary_key or not f.auto_created)
                        for item in serializer.validated_data
                    ]
                    with _conn.cursor() as _cur:
                        _cur.executemany(sql, rows)
                    processed_count += len(rows)
                    logger.info(f"{self.record_type} - Successfully processed chunk {chunk_num} ({len(rows)} records)")
                except Exception as e:
                    logger.error(f"{self.record_type} - Database error in chunk {chunk_num}: {str(e)}")
                    logger.error(traceback.format_exc())
                    # Try individual record processing for this chunk
                    individual_count = self.process_individual_records(cleaned_chunk)
                    processed_count += individual_count
            else:
                logger.error(f"{self.record_type} - Serialization failed for chunk {chunk_num}")
                # Process individual records to identify specific issues
                individual_count = self.process_individual_records(cleaned_chunk)
                processed_count += individual_count
        
        return processed_count, failed_records
    
    def process_individual_records(self, records):
        """Process records individually to identify specific issues"""
        processed_count = 0
        
        for idx, record in enumerate(records):
            try:
                serializer = self.serializer_class(data=record)
                if serializer.is_valid():
                    model_instance = self.model(**serializer.validated_data)
                    model_instance.save()
                    processed_count += 1
                else:
                    logger.error(f"{self.record_type} - Record {idx} validation failed: {serializer.errors}")
                    logger.error(f"{self.record_type} - Problematic record: {json.dumps(record, indent=2, default=str)}")
            except Exception as e:
                logger.error(f"{self.record_type} - Exception processing record {idx}: {str(e)}")
                logger.error(f"{self.record_type} - Record data: {json.dumps(record, indent=2, default=str)}")
        
        return processed_count
    
    def post(self, request):
        data = request.data
        
        # Validate input
        if not isinstance(data, list):
            logger.error(f"{self.record_type} - Expected a list of records")
            return Response({"error": "Expected a list of records"}, status=400)
        
        if not data:
            logger.warning(f"{self.record_type} - Received empty data")
            return Response({"message": f"{self.record_type} - No records to process"}, status=200)
        
        logger.info(f"{self.record_type} - Received {len(data)} records")
        
        # Log sample records
        for i, sample in enumerate(data[:2]):
            logger.info(f"{self.record_type} - Sample Record {i+1}: {json.dumps(sample, indent=2, default=str)}")
        
        try:
            with transaction.atomic():
                # Clear existing records — use raw SQL to avoid ORM id lookup on managed=False tables
                from django.db import connection as _conn
                with _conn.cursor() as _cur:
                    _cur.execute(f"DELETE FROM {self.model._meta.db_table}")
                
                # Process records in chunks
                processed_count, failed_records = self.process_in_chunks(data)
                
                # Log results
                logger.info(f"{self.record_type} - Successfully processed {processed_count} out of {len(data)} records")
                
                if failed_records:
                    logger.warning(f"{self.record_type} - {len(failed_records)} records failed validation")
                    for failed in failed_records[:5]:  # Log first 5 failed records
                        logger.warning(f"Failed record at index {failed['index']}: {failed['error']}")
                
                return Response({
                    "message": f"{self.record_type} records processed",
                    "processed_count": processed_count,
                    "total_count": len(data),
                    "failed_count": len(failed_records)
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            logger.error(f"{self.record_type} - Critical error: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({"error": "Internal server error"}, status=500)
    
    def get(self, request):
        records = self.model.objects.all()
        serializer = self.serializer_class(records, many=True)
        return Response(serializer.data)


class IMC1LedgersView(BaseLedgersView):
    model = IMC1RecordLedgers
    serializer_class = IMC1LedgersSerializer
    record_type = "IMC1 Ledgers"


class IMC2LedgersView(BaseLedgersView):
    model = IMC2RecordLedgers
    serializer_class = IMC2LedgersSerializer
    record_type = "IMC2 Ledgers"


class SysmacLedgersView(BaseLedgersView):
    model = SysmacRecordLedgers
    serializer_class = SysmacLedgersSerializer
    record_type = "Sysmac Ledgers"


class DQLedgersView(BaseLedgersView):
    model = DQRecordsLedgers
    serializer_class = DQLedgersSerializer
    record_type = "DQ Ledgers"


class PlanetLedgersView(BaseLedgersView):
    model = PlanetLedgers
    serializer_class = PlanetLedgersSerializer
    record_type = "Planet Ledgers"


class IMC1RecordView(APIView):
    def post(self, request):
        logger.info(f"IMC1 - Received {len(request.data)} records")
        serializer = IMC1Serializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    IMC1Record.objects.all().delete()
                    records = [IMC1Record(**item) for item in serializer.validated_data]
                    IMC1Record.objects.bulk_create(records, batch_size=1000)
                logger.info(f"Saved {len(records)} IMC-1 records")
                return Response({"message": "IMC-1 records saved"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"IMC1 DB error: {e}")
                logger.error(traceback.format_exc())
                return Response({"error": "Database error", "detail": str(e)}, status=500)
        
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
            try:
                with transaction.atomic():
                    IMC2Record.objects.all().delete()
                    records = [IMC2Record(**item) for item in serializer.validated_data]
                    IMC2Record.objects.bulk_create(records, batch_size=1000)
                logger.info(f"Saved {len(records)} IMC-2 records")
                return Response({"message": "IMC-2 records saved"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"IMC2 DB error: {e}")
                logger.error(traceback.format_exc())
                return Response({"error": "Database error", "detail": str(e)}, status=500)
        
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
            try:
                with transaction.atomic():
                    SysmacRecord.objects.all().delete()
                    records = [SysmacRecord(**item) for item in serializer.validated_data]
                    SysmacRecord.objects.bulk_create(records, batch_size=1000)
                logger.info(f"Saved {len(records)} Sysmac records")
                return Response({"message": "Sysmac records saved"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Sysmac DB error: {e}")
                logger.error(traceback.format_exc())
                return Response({"error": "Database error", "detail": str(e)}, status=500)
        
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
            try:
                with transaction.atomic():
                    DQRecord.objects.all().delete()
                    records = [DQRecord(**item) for item in serializer.validated_data]
                    DQRecord.objects.bulk_create(records, batch_size=1000)
                logger.info(f"Saved {len(records)} DQ records")
                return Response({"message": "DQ records saved"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"DQ DB error: {e}")
                logger.error(traceback.format_exc())
                return Response({"error": "Database error", "detail": str(e)}, status=500)
        
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
                    from django.db import connection as _conn
                    with _conn.cursor() as _cur:
                        _cur.execute("DELETE FROM planet_master")
                        fields = [f.column for f in PlanetMaster._meta.concrete_fields if not f.primary_key or not f.auto_created]
                        placeholders = ', '.join(['%s'] * len(fields))
                        col_names = ', '.join(fields)
                        rows = [tuple(item.get(f.attname, None) for f in PlanetMaster._meta.concrete_fields if not f.primary_key or not f.auto_created) for item in serializer.validated_data]
                        _cur.executemany(f"INSERT INTO planet_master ({col_names}) VALUES ({placeholders})", rows)
                records = serializer.validated_data
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
    """
    POST  – deletes planet_clients rows for the given client_id, then inserts
            fresh records tagged with that client_id.
            client_id is read from X-Client-ID header or ?client_id= query param.
    GET   – returns records, optionally filtered by ?client_id=.
    DELETE– removes all rows for a client_id (truncate step from sync tool).
    """

    def _get_client_id(self, request):
        return (
            request.headers.get("X-Client-ID", "").strip()
            or request.query_params.get("client_id", "").strip()
        )

    def post(self, request):
        try:
            client_id = self._get_client_id(request)
            data = request.data

            if not isinstance(data, list):
                return Response({"error": "Expected a list of records"}, status=400)
            if not data:
                return Response({"message": "No records to process"}, status=200)

            logger.info(f"PLANET_CLIENTS - Received {len(data)} records "
                        f"(client_id={client_id!r})")

            for i, record in enumerate(data[:2]):
                logger.info(f"Sample record {i}: {json.dumps(record, indent=2, default=str)}")

            # ── Build column list directly from the model (skip auto PK) ──────
            all_fields = [
                f for f in PlanetClient._meta.concrete_fields
                if not f.primary_key or not f.auto_created
            ]
            col_names    = ', '.join(f.column for f in all_fields)
            placeholders = ', '.join(['%s'] * len(all_fields))
            insert_sql   = (
                f"INSERT INTO planet_clients ({col_names}) VALUES ({placeholders})"
            )

            # ── Coerce each incoming record directly — no serializer ──────────
            # Bypassing PlanetClientsSerializer.is_valid() here is intentional.
            # DRF's ModelSerializer with primary_key=True on `code` runs a
            # UniqueValidator against the DB for every row, rejecting any code
            # that already exists — even though we are about to delete those rows.
            # That caused all 314 existing-code rows to fail validation silently,
            # leaving only the 15 brand-new codes to insert (329 fetched → 15 saved).
            # Raw SQL bypasses UniqueValidator entirely and inserts all rows.
            from datetime import date as _date
            rows    = []
            skipped = 0
            for rec in data:
                code = str(rec.get("code", "") or "").strip()
                if not code:
                    skipped += 1
                    continue

                row = []
                for f in all_fields:
                    val = rec.get(f.attname, rec.get(f.column))

                    # Inject client_id when missing
                    if f.attname == "client_id" and (val is None or val == ""):
                        val = client_id

                    # Coerce installationdate -> YYYY-MM-DD or None
                    if f.attname == "installationdate" and val:
                        if isinstance(val, _date):
                            val = val.isoformat()
                        elif isinstance(val, str) and val.strip():
                            val = val[:10]
                        else:
                            val = None

                    # Blank strings -> None for nullable columns
                    if val == "" and f.null:
                        val = None

                    row.append(val)
                rows.append(tuple(row))

            if skipped:
                logger.warning(f"PLANET_CLIENTS - Skipped {skipped} records missing 'code'")

            if not rows:
                return Response(
                    {"message": "No valid records to insert", "skipped": skipped},
                    status=200,
                )

            # ── Atomic: delete this client's rows, then insert all ────────────
            with transaction.atomic():
                from django.db import connection as _conn
                with _conn.cursor() as _cur:
                    if client_id:
                        _cur.execute(
                            "DELETE FROM planet_clients WHERE client_id = %s",
                            [client_id],
                        )
                        logger.info(
                            f"PLANET_CLIENTS - Deleted existing rows for client_id={client_id!r}"
                        )
                    else:
                        _cur.execute("DELETE FROM planet_clients")
                        logger.info("PLANET_CLIENTS - Deleted ALL existing rows (no client_id)")

                    _cur.executemany(insert_sql, rows)

            logger.info(
                f"PLANET_CLIENTS - Saved {len(rows)} records for client_id={client_id!r} "
                f"(skipped {skipped} without code)"
            )
            return Response(
                {
                    "message":   "PLANET_CLIENTS records saved",
                    "count":     len(rows),
                    "skipped":   skipped,
                    "client_id": client_id,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.error(f"PLANET_CLIENTS Exception: {str(e)}")
            logger.error(traceback.format_exc())
            if request.data:
                logger.error(f"Sample record: {json.dumps(request.data[0], indent=2, default=str)}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        client_id = self._get_client_id(request)
        from django.db import connection as _conn
        with _conn.cursor() as _cur:
            if client_id:
                _cur.execute("DELETE FROM planet_clients WHERE client_id = %s", [client_id])
                deleted = _cur.rowcount
            else:
                _cur.execute("DELETE FROM planet_clients")
                deleted = _cur.rowcount
        logger.info(f"PLANET_CLIENTS - Deleted {deleted} rows (client_id={client_id!r})")
        return Response({"deleted": deleted, "client_id": client_id}, status=200)

    def get(self, request):
        client_id = self._get_client_id(request)
        qs = (PlanetClient.objects.filter(client_id=client_id)
              if client_id else PlanetClient.objects.all())
        serializer = PlanetClientsSerializer(qs, many=True)
        return Response(serializer.data)


class BaseInvMastView(APIView):
    """Base class for all invoice master views with common functionality"""
    
    model = None
    serializer_class = None
    record_type = None
    
    def clean_record(self, record):
        """Clean and validate individual record before serialization"""
        cleaned = record.copy()
        
        # Handle date field
        if 'invdate' in cleaned:
            if cleaned['invdate'] is None or cleaned['invdate'] == '':
                cleaned['invdate'] = None
            elif isinstance(cleaned['invdate'], str):
                date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S', '%d-%m-%Y']
                for fmt in date_formats:
                    try:
                        parsed_date = datetime.strptime(cleaned['invdate'], fmt).date()
                        cleaned['invdate'] = parsed_date.strftime('%Y-%m-%d')
                        break
                    except ValueError:
                        continue
                else:
                    logger.warning(f"Could not parse invdate: {cleaned['invdate']}")
                    cleaned['invdate'] = None
        
        # Handle decimal fields
        decimal_fields = ['nettotal', 'paid']
        for field in decimal_fields:
            if field in cleaned:
                if cleaned[field] is None or cleaned[field] == '':
                    cleaned[field] = None
                else:
                    try:
                        cleaned[field] = str(Decimal(str(cleaned[field])))
                    except (ValueError, InvalidOperation, TypeError):
                        logger.warning(f"Could not convert {field} to decimal: {cleaned[field]}")
                        cleaned[field] = None
        
        # Handle string fields
        string_fields = ['modeofpayment', 'customerid', 'bill_ref']
        for field in string_fields:
            if field in cleaned:
                if cleaned[field] is None:
                    cleaned[field] = ''
                else:
                    cleaned[field] = str(cleaned[field]).strip()
        
        return cleaned
    
    def process_in_chunks(self, data, chunk_size=500):
        """Process data in smaller chunks"""
        total_records = len(data)
        processed_count = 0
        failed_records = []
        
        logger.info(f"{self.record_type} - Processing {total_records} records in chunks of {chunk_size}")
        
        for i in range(0, total_records, chunk_size):
            chunk = data[i:i + chunk_size]
            chunk_num = (i // chunk_size) + 1
            
            logger.info(f"{self.record_type} - Processing chunk {chunk_num} ({len(chunk)} records)")
            
            # Clean each record in the chunk
            cleaned_chunk = []
            for idx, record in enumerate(chunk):
                cleaned_record = self.clean_record(record)
                if cleaned_record is not None:
                    cleaned_chunk.append(cleaned_record)
                else:
                    failed_records.append({
                        'index': i + idx,
                        'record': record,
                        'error': 'Invalid record data'
                    })
            
            if not cleaned_chunk:
                logger.warning(f"{self.record_type} - Chunk {chunk_num} has no valid records")
                continue
            
            # Try to serialize the chunk
            serializer = self.serializer_class(data=cleaned_chunk, many=True)
            if serializer.is_valid():
                try:
                    records = [self.model(**item) for item in serializer.validated_data]
                    self.model.objects.bulk_create(records, batch_size=1000)
                    processed_count += len(records)
                    logger.info(f"{self.record_type} - Successfully processed chunk {chunk_num} ({len(records)} records)")
                except Exception as e:
                    logger.error(f"{self.record_type} - Database error in chunk {chunk_num}: {str(e)}")
                    individual_count = self.process_individual_records(cleaned_chunk)
                    processed_count += individual_count
            else:
                logger.error(f"{self.record_type} - Serialization failed for chunk {chunk_num}")
                individual_count = self.process_individual_records(cleaned_chunk)
                processed_count += individual_count
        
        return processed_count, failed_records
    
    def process_individual_records(self, records):
        """Process records individually to identify specific issues"""
        processed_count = 0
        
        for idx, record in enumerate(records):
            try:
                serializer = self.serializer_class(data=record)
                if serializer.is_valid():
                    model_instance = self.model(**serializer.validated_data)
                    model_instance.save()
                    processed_count += 1
                else:
                    logger.error(f"{self.record_type} - Record {idx} validation failed: {serializer.errors}")
            except Exception as e:
                logger.error(f"{self.record_type} - Exception processing record {idx}: {str(e)}")
        
        return processed_count
    
    def post(self, request):
        data = request.data
        
        if not isinstance(data, list):
            logger.error(f"{self.record_type} - Expected a list of records")
            return Response({"error": "Expected a list of records"}, status=400)
        
        if not data:
            logger.warning(f"{self.record_type} - Received empty data")
            return Response({"message": f"{self.record_type} - No records to process"}, status=200)
        
        logger.info(f"{self.record_type} - Received {len(data)} records")
        
        # Log sample records
        for i, sample in enumerate(data[:2]):
            logger.info(f"{self.record_type} - Sample Record {i+1}: {json.dumps(sample, indent=2, default=str)}")
        
        try:
            with transaction.atomic():
                self.model.objects.all().delete()
                processed_count, failed_records = self.process_in_chunks(data)
                
                logger.info(f"{self.record_type} - Successfully processed {processed_count} out of {len(data)} records")
                
                return Response({
                    "message": f"{self.record_type} records processed",
                    "processed_count": processed_count,
                    "total_count": len(data),
                    "failed_count": len(failed_records)
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            logger.error(f"{self.record_type} - Critical error: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({"error": "Internal server error"}, status=500)
    
    def get(self, request):
        records = self.model.objects.all()
        serializer = self.serializer_class(records, many=True)
        return Response(serializer.data)


class PlanetInvMastView(BaseInvMastView):
    model = PlanetInvMast
    serializer_class = PlanetInvMastSerializer
    record_type = "Planet InvMast"


class IMC1InvMastView(BaseInvMastView):
    model = IMC1InvMast
    serializer_class = IMC1InvMastSerializer
    record_type = "IMC1 InvMast"


class IMC2InvMastView(BaseInvMastView):
    model = IMC2InvMast
    serializer_class = IMC2InvMastSerializer
    record_type = "IMC2 InvMast"


class SysmacInvMastView(BaseInvMastView):
    model = SysmacInvMast
    serializer_class = SysmacInvMastSerializer
    record_type = "Sysmac InvMast"


class DQInvMastView(BaseInvMastView):
    model = DQInvMast
    serializer_class = DQInvMastSerializer
    record_type = "DQ InvMast"



class AccMasterView(APIView):
    """
    POST  – deletes acc_master rows for the given client_id, then bulk-inserts
            fresh records tagged with that client_id.
            client_id is read from the X-Client-ID request header (or query param
            ?client_id=).  If omitted, all rows are replaced (backward-compatible).
    GET   – returns records, optionally filtered by ?client_id=.
    DELETE– removes all rows for a client_id (called by the sync tool before re-push).
    """

    def _get_client_id(self, request):
        return (
            request.headers.get("X-Client-ID", "").strip()
            or request.query_params.get("client_id", "").strip()
        )

    def post(self, request):
        data = request.data
        client_id = self._get_client_id(request)

        if not isinstance(data, list):
            logger.error("AccMaster - Expected a list of records")
            return Response({"error": "Expected a list of records"}, status=400)

        if not data:
            logger.warning("AccMaster - Received empty payload")
            return Response({"message": "No records to process"}, status=200)

        logger.info(f"AccMaster - Received {len(data)} records (client_id={client_id!r})")

        # Inject client_id into every record so the serializer sees it
        tagged = []
        for rec in data:
            r = dict(rec)
            r.setdefault("client_id", client_id)
            tagged.append(r)

        for i, sample in enumerate(tagged[:2]):
            logger.info(f"AccMaster - Sample record {i + 1}: "
                        f"{json.dumps(sample, indent=2, default=str)}")

        serializer = AccMasterSerializer(data=tagged, many=True)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # Delete only this client's rows (or all if no client_id)
                    if client_id:
                        AccMaster.objects.filter(client_id=client_id).delete()
                    else:
                        AccMaster.objects.all().delete()
                    records = [AccMaster(**item) for item in serializer.validated_data]
                    AccMaster.objects.bulk_create(records, batch_size=1000)
                logger.info(f"AccMaster - Saved {len(records)} records for client_id={client_id!r}")
                return Response(
                    {"message": "AccMaster records saved", "count": len(records),
                     "client_id": client_id},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                logger.error(f"AccMaster - DB error: {e}")
                logger.error(traceback.format_exc())
                return Response({"error": "Database error"}, status=500)

        errors_sample = list(serializer.errors)[:5]
        logger.error(f"AccMaster - Validation errors (first 5): "
                     f"{json.dumps(errors_sample, indent=2, default=str)}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        client_id = self._get_client_id(request)
        if client_id:
            deleted, _ = AccMaster.objects.filter(client_id=client_id).delete()
        else:
            deleted, _ = AccMaster.objects.all().delete()
        logger.info(f"AccMaster - Deleted {deleted} rows (client_id={client_id!r})")
        return Response({"deleted": deleted, "client_id": client_id}, status=200)

    def get(self, request):
        client_id = self._get_client_id(request)
        qs = AccMaster.objects.filter(client_id=client_id) if client_id else AccMaster.objects.all()
        serializer = AccMasterSerializer(qs, many=True)
        return Response(serializer.data)


class AccProductView(APIView):
    """
    POST  – deletes acc_product rows for the given client_id, then bulk-inserts
            fresh records tagged with that client_id.
    GET   – returns records, optionally filtered by ?client_id=.
    DELETE– removes all rows for a client_id.
    """

    def _get_client_id(self, request):
        return (
            request.headers.get("X-Client-ID", "").strip()
            or request.query_params.get("client_id", "").strip()
        )

    def post(self, request):
        data = request.data
        client_id = self._get_client_id(request)

        if not isinstance(data, list):
            logger.error("AccProduct - Expected a list of records")
            return Response({"error": "Expected a list of records"}, status=400)

        if not data:
            logger.warning("AccProduct - Received empty payload")
            return Response({"message": "No records to process"}, status=200)

        logger.info(f"AccProduct - Received {len(data)} records (client_id={client_id!r})")

        tagged = []
        for rec in data:
            r = dict(rec)
            r.setdefault("client_id", client_id)
            tagged.append(r)

        for i, sample in enumerate(tagged[:2]):
            logger.info(f"AccProduct - Sample record {i + 1}: "
                        f"{json.dumps(sample, indent=2, default=str)}")

        serializer = AccProductSerializer(data=tagged, many=True)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    if client_id:
                        AccProduct.objects.filter(client_id=client_id).delete()
                    else:
                        AccProduct.objects.all().delete()
                    records = [AccProduct(**item) for item in serializer.validated_data]
                    AccProduct.objects.bulk_create(records, batch_size=1000)
                logger.info(f"AccProduct - Saved {len(records)} records for client_id={client_id!r}")
                return Response(
                    {"message": "AccProduct records saved", "count": len(records),
                     "client_id": client_id},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                logger.error(f"AccProduct - DB error: {e}")
                logger.error(traceback.format_exc())
                return Response({"error": "Database error"}, status=500)

        errors_sample = list(serializer.errors)[:5]
        logger.error(f"AccProduct - Validation errors (first 5): "
                     f"{json.dumps(errors_sample, indent=2, default=str)}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        client_id = self._get_client_id(request)
        if client_id:
            deleted, _ = AccProduct.objects.filter(client_id=client_id).delete()
        else:
            deleted, _ = AccProduct.objects.all().delete()
        logger.info(f"AccProduct - Deleted {deleted} rows (client_id={client_id!r})")
        return Response({"deleted": deleted, "client_id": client_id}, status=200)

    def get(self, request):
        client_id = self._get_client_id(request)
        qs = AccProduct.objects.filter(client_id=client_id) if client_id else AccProduct.objects.all()
        serializer = AccProductSerializer(qs, many=True)
        return Response(serializer.data)