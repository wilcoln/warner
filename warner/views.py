from django.shortcuts import render, redirect, HttpResponse
from warner.models import *
from datetime import date
from datetime import datetime
from datetime import timedelta
import types


def create_epochs_up_to(end_date):
    Epoch.objects.all().delete()
    current_date = datetime.now().date() + timedelta(days=-10)
    while current_date < end_date:
        epoch = Epoch()
        epoch.date = current_date
        epoch.save()
        current_date = current_date + timedelta(days=1)


def compute_balance(start, end):
    epoch = start
    result = epoch.balance()
    while epoch.date < end.date:
        epoch = epoch.next()
        result += epoch.balance()
    return result


def home(request):
    last_epoch = Epoch.objects.last()
    today_epoch = Epoch.objects.filter(date=datetime.now().date()).first()
    balance = types.SimpleNamespace()
    balance.today = today_epoch.balance()
    balance.period = last_epoch.balance()
    epochs = Epoch.objects.all()
    return render(request, 'home.html', {'epochs': epochs, 'balance': balance})


def view_epoch(request, id):
    last_epoch = Epoch.objects.last()
    today_epoch = Epoch.objects.filter(date=datetime.now().date()).first()
    epoch = Epoch.objects.get(pk=id)
    balance = types.SimpleNamespace()
    balance.today = today_epoch.balance()
    balance.period = last_epoch.balance()
    epochs = Epoch.objects.all()
    return render(request, 'home.html', {'epochs': epochs, 'balance': balance, 'forecast_epoch': epoch})