from django import forms
from warner.models import Epoch, Forecast
import datetime


class ForecastForm(forms.Form):
    is_inevitable = forms.BooleanField(label='Inevitable', required=False)
    amount = forms.FloatField(label='Amount')
    reason = forms.CharField(label='Reason', required=False)
    epochs_select = forms.ModelMultipleChoiceField(queryset=Epoch.objects.filter(date__gte=datetime.datetime.now().date()))


class TransactionForm(forms.Form):
    amount = forms.FloatField(label='Amount')
    reason = forms.CharField(label='Reason', required=False)
    epoch_select = forms.ModelChoiceField(queryset=Epoch.objects.filter(date__lte=datetime.datetime.now().date()).order_by('-date'))
    forecast_select = forms.ModelChoiceField(queryset=Forecast.objects.all())
