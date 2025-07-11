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
