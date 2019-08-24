# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import datetime
from django.db.models import Sum


class Tag(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tag'


class Forecast(models.Model):
    is_inevitable = models.BooleanField(default=False)
    amount = models.FloatField()
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.amount) + ' ' + self.reason

    class Meta:
        db_table = 'forecast'


class Epoch(models.Model):
    is_useful = models.BooleanField(default=False)
    date = models.DateField()
    forecast_set = models.ManyToManyField(Forecast, blank=True)

    def __str__(self):
        return str(self.date.strftime("%A %d %B, %Y"))

    def prev(self):
        return Epoch.objects.filter(is_useful=True, date__lt=self.date).order_by('date').last()

    def next(self):
        return Epoch.objects.filter(is_useful=True, date__gt=self.date).order_by('date').first()

    def is_over(self):
        return self.date < datetime.datetime.now().date()

    def is_ongoing(self):
        return self.date == datetime.datetime.now().date()

    def income(self):
        result = 0
        if self.is_useful:
            val = self.transaction_set.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum']
            result += val if val is not None else 0
            if not self.is_over():
                val = self.forecast_set.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum']
                result += val if val is not None else 0
        return result

    def outgo(self):
        result = 0
        if self.is_useful:
            val = self.transaction_set.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum']
            result += val if val is not None else 0
            if not self.is_over():
                val = self.forecast_set.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum']
                result += val if val is not None else 0
        return -result

    def balance(self):
        result = 0
        if self.is_useful:
            val = self.transaction_set.all().aggregate(Sum('amount'))['amount__sum']
            result += val if val is not None else 0
            if not self.is_over():
                if self.is_ongoing():
                    val = self.forecast_set.filter(transaction__isnull=True).aggregate(Sum('amount'))['amount__sum']
                else:
                    val = self.forecast_set.all().aggregate(Sum('amount'))['amount__sum']
                result += val if val is not None else 0
        if self.prev():
            result += self.prev().balance()
        return result

    class Meta:
        db_table = 'epoch'


class Transaction(models.Model):
    amount = models.FloatField()
    epoch = models.ForeignKey(Epoch, on_delete=models.CASCADE)
    forecast = models.ForeignKey(Forecast, null=True, blank=True, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.epoch) + ', ' + str(self.amount) + ', ' + self.reason

    class Meta:
        db_table = 'transaction'
