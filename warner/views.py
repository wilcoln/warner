from django.shortcuts import render, redirect, HttpResponse
from warner.models import *
from datetime import datetime
from datetime import timedelta
import types
from warner.forms import *


def create_epochs_up_to(end_date):
    Epoch.objects.all().delete()
    current_date = datetime.now().date() + timedelta(days=-10)
    while current_date < end_date:
        epoch = Epoch()
        epoch.date = current_date
        epoch.save()
        current_date = current_date + timedelta(days=1)


def home(request):
    last_epoch = Epoch.objects.last()
    today_epoch = Epoch.objects.filter(date=datetime.datetime.now().date()).first()
    balance = types.SimpleNamespace()
    balance.today = today_epoch.balance()
    balance.period = last_epoch.balance()
    epochs = Epoch.objects.all()
    return render(request, 'home.html', {'epochs': epochs, 'balance': balance})


def view_epoch(request, id):
    epochs = Epoch.objects.all()
    epoch = epochs.get(pk=id)
    balance = types.SimpleNamespace()
    balance.epoch = epoch.balance()
    return render(request, 'home.html', {'epochs': epochs, 'balance': balance, 'current_epoch': epoch})

# def view_epoch(request, id):
#     epochs = Epoch.objects.all()
#     epoch = epochs.get(pk=id)
#     last_epoch = epochs.last()
#     today_epoch = epochs.filter(date=datetime.datetime.now().date()).first()
#     balance = types.SimpleNamespace()
#     balance.today = today_epoch.balance()
#     balance.period = last_epoch.balance()
#     balance.epoch = epoch.balance()
#     return render(request, 'home.html', {'epochs': epochs, 'balance': balance, 'current_epoch': epoch})


def add_forecast(request):
    forecast_form = ForecastForm()
    return render(request, 'add_forecast.html', {'forecast_form': forecast_form})


def save_forecast(request):
    if request.method == 'POST':
        form = ForecastForm(request.POST)
        if form.is_valid():
            forecast = Forecast()
            forecast.is_inevitable = form.cleaned_data['is_inevitable']
            forecast.amount = form.cleaned_data['amount']
            forecast.reason = form.cleaned_data['reason']
            forecast.save()

            epochs = form.cleaned_data['epochs_select']
            for epoch in epochs:
                epoch.forecast_set.add(forecast)
                epoch.is_useful = True
                epoch.save()
    return redirect('home')


def mark_as_useful(request, id):
    epoch = Epoch.objects.get(pk=id)
    epoch.is_useful = True
    epoch.save()
    return redirect('home')


def save_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = Transaction()
            transaction.amount = form.cleaned_data['amount']
            transaction.reason = form.cleaned_data['reason']
            transaction.epoch = form.cleaned_data['epoch_select']
            transaction.epoch.is_useful = True
            transaction.epoch.save()
            transaction.forecast = form.cleaned_data['forecast_select']
            transaction.save()
    return redirect('home')


def index_transaction(request):
    transactions = Transaction.objects.all()
    return render(request, 'list.html', {'list': transactions})


def index_forecast(request):
    forecasts = Forecast.objects.all()
    return render(request, 'list.html', {'list': forecasts})


def add_transaction(request):
    transaction_form = TransactionForm(initial={'epoch_select': Epoch.objects.filter(date=datetime.datetime.now().date()).first()})
    return render(request, 'add_transaction.html', {'transaction_form': transaction_form})

