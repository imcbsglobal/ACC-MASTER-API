from django.db import models


class IMC1Record(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    opening_balance = models.FloatField()
    debit = models.FloatField()
    credit = models.FloatField()
    place = models.CharField(max_length=200, null=True, blank=True)
    phone2 = models.CharField(max_length=50, null=True, blank=True)
    openingdepartment = models.CharField(max_length=100, blank=True)
    synced_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'syncdata_imc1record'
        # managed = False

class IMC1RecordLedgers(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    particulars = models.CharField(max_length=250, null=True, blank=True)
    debit = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    credit = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    entry_mode = models.CharField(max_length=30, null=True, blank=True)
    entry_date = models.DateField(null=True, blank=True)
    voucher_no = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    narration = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = "syncdata_imc1recordledgers"
        managed = False

class IMC2Record(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    opening_balance = models.FloatField()
    debit = models.FloatField()
    credit = models.FloatField()
    place = models.CharField(max_length=200, null=True, blank=True)
    phone2 = models.CharField(max_length=50, null=True, blank=True)
    openingdepartment = models.CharField(max_length=100, blank=True)
    synced_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'syncdata_imc2record'
        # managed = False

class IMC2RecordLedgers(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    particulars = models.CharField(max_length=250, null=True, blank=True)
    debit = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    credit = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    entry_mode = models.CharField(max_length=30, null=True, blank=True)
    entry_date = models.DateField(null=True, blank=True)
    voucher_no = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    narration = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = "syncdata_imc2recordledgers"
        managed = False


class SysmacRecord(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    opening_balance = models.FloatField()
    debit = models.FloatField()
    credit = models.FloatField()
    place = models.CharField(max_length=200,null=True, blank=True)
    phone2 = models.CharField(max_length=50, null=True, blank=True)
    openingdepartment = models.CharField(max_length=100, blank=True)
    synced_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'syncdata_sysmacinfo'
        # managed = False

class SysmacRecordLedgers(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    particulars = models.CharField(max_length=250, null=True, blank=True)
    debit = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    credit = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    entry_mode = models.CharField(max_length=30, null=True, blank=True)
    entry_date = models.DateField(null=True, blank=True)
    voucher_no = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    narration = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = "syncdata_sysmacinfoledgers"
        managed = False


class DQRecord(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    opening_balance = models.FloatField()
    debit = models.FloatField()
    credit = models.FloatField()
    place = models.CharField(max_length=200, null=True, blank=True)
    phone2 = models.CharField(max_length=50, null=True, blank=True)
    openingdepartment = models.CharField(max_length=100, blank=True)
    synced_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'syncdata_dqrecord'
        # managed = False

class DQRecordsLedgers(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    particulars = models.CharField(max_length=250, null=True, blank=True)
    debit = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    credit = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    entry_mode = models.CharField(max_length=30, null=True, blank=True)
    entry_date = models.DateField(null=True, blank=True)
    voucher_no = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    narration = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = "syncdata_dqrecordledgers"
        managed = False

class PlanetClient(models.Model):
    code = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    software = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    installationdate = models.DateField(blank=True, null=True)
    priorty = models.IntegerField(blank=True, null=True)
    directdealing = models.CharField(max_length=50, blank=True, null=True)
    rout = models.CharField(max_length=100, blank=True, null=True)
    amc = models.CharField(max_length=50, blank=True, null=True)
    amcamt = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True)
    accountcode = models.CharField(max_length=50, blank=True, null=True)
    address3 = models.TextField(blank=True, null=True)
    lictype = models.CharField(max_length=50, blank=True, null=True)
    clients = models.IntegerField(blank=True, null=True)
    sp = models.IntegerField(blank=True, null=True)
    nature = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False  
        db_table = 'planet_clients'


class PlanetMaster(models.Model):
    code = models.CharField(max_length=30, blank=False, null=False)
    name = models.CharField(max_length=250, blank=False, null=False)
    super_code = models.CharField(max_length=5, blank=True, null=True)
    opening_balance = models.DecimalField(
        max_digits=12, decimal_places=3, blank=True, null=True)
    debit = models.DecimalField(
        max_digits=16, decimal_places=3, blank=True, null=True)
    credit = models.DecimalField(
        max_digits=16, decimal_places=3, blank=True, null=True)
    place = models.CharField(max_length=60, blank=True, null=True)
    phone2 = models.CharField(max_length=60, blank=True, null=True)
    openingdepartment = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False  
        db_table = 'planet_master'

class PlanetLedgers(models.Model):
    code = models.CharField(max_length=30 , primary_key=True)
    particulars = models.CharField(max_length=250, null=True, blank=True)
    debit = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    credit = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    entry_mode = models.CharField(max_length=30, null=True, blank=True)
    entry_date = models.DateField(null=True, blank=True)
    voucher_no = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    narration = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = "planet_ledgers"
        managed = False



class BaseInvMastModel(models.Model):
    """Base model for all invoice master tables with common fields"""
    modeofpayment = models.CharField(max_length=1, null=True, blank=True)
    customerid = models.CharField(max_length=50, primary_key=True)  # Increased from 5 to 50
    invdate = models.DateField(null=True, blank=True)
    nettotal = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    paid = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    bill_ref = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True

class ManagedInvMastModel(BaseInvMastModel):
    """Base model for managed tables with synced_at field"""
    
    class Meta:
        abstract = True
        managed = True

class PlanetInvMast(BaseInvMastModel):  
    class Meta:
        db_table = 'planet_invmast'
        managed = True

class IMC1InvMast(ManagedInvMastModel):  
    class Meta:
        db_table = 'syncdata_imc1mast'
        managed = True

class IMC2InvMast(ManagedInvMastModel):  
    class Meta:
        db_table = 'syncdata_imc2mast'
        managed = True

class SysmacInvMast(ManagedInvMastModel):  
    class Meta:
        db_table = 'syncdata_sysmacinfo_mast'
        managed = True

class DQInvMast(ManagedInvMastModel):  
    class Meta:
        db_table = 'syncdata_dqrecord_mast'
        managed = True