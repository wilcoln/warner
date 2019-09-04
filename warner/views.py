from django.shortcuts import render, redirect, HttpResponse
from warner.models import *
from datetime import datetime
from datetime import timedelta
import types
from warner.forms import *


def create_episodes_between(start_date, end_date):
    current_date = start_date
    while current_date < end_date:
        episode = Episode()
        episode.date = current_date
        episode.save()
        current_date = current_date + timedelta(days=1)


def create_episodes(request):
    create_episodes_between(datetime.datetime.now().date() + timedelta(days=-10), datetime.date(2020, 9, 14))
    return redirect('home')


def home(request):
    last_episode = Episode.objects.last()
    today_episode = Episode.objects.filter(date=datetime.datetime.now().date()).first()
    balance = types.SimpleNamespace()
    balance.today = today_episode.balance()
    balance.period = last_episode.balance()
    episodes = Episode.objects.all()
    return render(request, 'home.html', {'episodes': episodes, 'balance': balance})


def view_episode(request, id):
    episodes = Episode.objects.all()
    episode = episodes.get(pk=id)
    balance = types.SimpleNamespace()
    balance.episode = episode.balance()
    return render(request, 'home.html', {'episodes': episodes, 'balance': balance, 'current_episode': episode})

# def view_episode(request, id):
#     episodes = Episode.objects.all()
#     episode = episodes.get(pk=id)
#     last_episode = episodes.last()
#     today_episode = episodes.filter(date=datetime.datetime.now().date()).first()
#     balance = types.SimpleNamespace()
#     balance.today = today_episode.balance()
#     balance.period = last_episode.balance()
#     balance.episode = episode.balance()
#     return render(request, 'home.html', {'episodes': episodes, 'balance': balance, 'current_episode': episode})


def edit_forecast(request, id):
    forecast = Forecast.objects.get(pk=id)
    forecast_form = ForecastForm(initial={
        'is_active': forecast.is_active,
        'amount': forecast.amount,
        'reason': forecast.reason,
        'episodes_select': forecast.episode_set.all(),
    })
    return render(request, 'edit_forecast.html', {'forecast_form': forecast_form, 'forecast': forecast})


def edit_transaction(request, id):
    transaction = Transaction.objects.get(pk=id)
    transaction_form = TransactionForm(initial={
        'amount': transaction.amount,
        'reason': transaction.reason,
        'episode_select': transaction.episode,
        'forecast_select': transaction.forecast
    })

    return render(request, 'edit_transaction.html', {'transaction_form': transaction_form, 'transaction': transaction})


def add_forecast(request):
    forecast_form = ForecastForm(initial={'is_active': True})
    return render(request, 'edit_forecast.html', {'forecast_form': forecast_form})


def save_forecast(request):
    if request.method == 'POST':
        form = ForecastForm(request.POST)
        if form.is_valid():
            if 'forecast-id' in request.POST.keys():
                forecast_id = int(request.POST['forecast-id'])
                forecast = Forecast.objects.get(pk=forecast_id)
                forecast.episode_set.clear()
            else:
                forecast = Forecast()
            forecast.is_active = form.cleaned_data['is_active']
            forecast.amount = form.cleaned_data['amount']
            forecast.reason = form.cleaned_data['reason']
            forecast.save()

            episodes = form.cleaned_data['episodes_select']
            for episode in episodes:
                episode.forecast_set.add(forecast)
                episode.is_useful = True
                episode.save()
    return redirect('home')


def mark_as_useful(request, id):
    episode = Episode.objects.get(pk=id)
    episode.is_useful = True
    episode.save()
    return redirect('home')


def save_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            if 'transaction-id' in request.POST.keys():
                transaction_id = int(request.POST['transaction-id'])
                transaction = Transaction.objects.get(pk=transaction_id)
            else:
                transaction = Transaction()
            transaction.amount = form.cleaned_data['amount']
            transaction.reason = form.cleaned_data['reason']
            transaction.episode = form.cleaned_data['episode_select']
            transaction.episode.is_useful = True
            transaction.episode.save()
            transaction.forecast = form.cleaned_data['forecast_select']
            transaction.save()
    return redirect('home')


def index_transaction(request):
    transactions = Transaction.objects.all()
    return render(request, 'index_transaction.html', {'list': transactions})


def index_forecast(request):
    forecasts = Forecast.objects.all()
    return render(request, 'index_forecast.html', {'list': forecasts})


def add_transaction(request):
    transaction_form = TransactionForm(initial={'episode_select': Episode.objects.filter(date=datetime.datetime.now().date()).first()})
    return render(request, 'edit_transaction.html', {'transaction_form': transaction_form})

