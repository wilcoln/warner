from django.shortcuts import render, redirect, HttpResponse
from warner.models import *
from datetime import date
from datetime import datetime
from datetime import timedelta


def create_epochs_up_to(end_date):
    Epoch.objects.all().delete()
    current_date = datetime.now().date()
    while current_date < end_date:
        epoch = Epoch()
        epoch.date = current_date
        epoch.save()
        current_date = current_date + timedelta(days=1)


def balance(start, end):
    epoch = start
    result = epoch.balance()
    while epoch.date < end.date:
        epoch = epoch.next()
        result += epoch.balance()
    return result


def welcome(request):
    first_epoch = Epoch.objects.first()
    last_epoch = Epoch.objects.last()
    return HttpResponse(balance(first_epoch, last_epoch))
    # courses = kc.fetch_courses()
    # return render(request, 'pages/welcome.html', {'courses': courses})
