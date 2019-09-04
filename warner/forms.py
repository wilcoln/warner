from django import forms
from warner.models import Episode, Forecast
import datetime


class ForecastForm(forms.Form):
    is_active = forms.BooleanField(label='Active', required=False)
    amount = forms.FloatField(label='Amount')
    reason = forms.CharField(label='Reason', required=False)
    episodes_select = forms.ModelMultipleChoiceField(queryset=Episode.objects.filter(date__gte=datetime.datetime.now().date()))


class TransactionForm(forms.Form):
    amount = forms.FloatField(label='Amount')
    reason = forms.CharField(label='Reason', required=False)
    episode_select = forms.ModelChoiceField(queryset=Episode.objects.filter(date__lte=datetime.datetime.now().date()).order_by('-date'))
    forecast_select = forms.ModelChoiceField(queryset=Forecast.objects.all(), required=False)
