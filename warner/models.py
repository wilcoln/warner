# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import datetime


class Tag(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tag'


class Prevision(models.Model):
    mandatory = models.BooleanField(default=False)
    amount = models.FloatField()
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.reason

    class Meta:
        db_table = 'prevision'


class Epoch(models.Model):
    date = models.DateField()
    prevision_set = models.ManyToManyField(Prevision, blank=True)

    def __str__(self):
        return str(self.date)

    def prev(self):
        return Epoch.objects.filter(date__lt=self.date).order_by('date').last()

    def next(self):
        return Epoch.objects.filter(date__gt=self.date).order_by('date').first()

    def is_over(self):
        return self.date < datetime.datetime.now().date()

    def is_ongoing(self):
        return self.date == datetime.datetime.now().date()

    def income(self):
        result = 0
        if self.is_over():
            for transaction in self.transaction_set.filter(amount__gt=0):
                result += transaction.amount
        else:
            for prevision in self.prevision_set.filter(amount__gt=0):
                result += prevision.amount
        return result

    def outgo(self):
        result = 0
        if self.is_over():
            for transaction in self.transaction_set.filter(amount__lt=0):
                result += transaction.amount
        else:
            for prevision in self.prevision_set.filter(amount__lt=0):
                result += prevision.amount
        return -result

    def balance(self):
        result = 0
        if self.is_over():
            for transaction in self.transaction_set.all():
                result += transaction.amount
            return result
        else:
            for prevision in self.prevision_set.all():
                result += prevision.amount
        if self.prev():
            result += self.prev().balance()
        return result

    class Meta:
        db_table = 'epoch'


class Transaction(models.Model):
    amount = models.FloatField()
    epoch = models.ForeignKey(Epoch, on_delete=models.CASCADE)
    prevision = models.ForeignKey(Prevision, null=True, blank=True, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.reason

    class Meta:
        db_table = 'transaction'
