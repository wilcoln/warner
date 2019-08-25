"""warner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from warner.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('epoch/<int:id>/', view_epoch, name='view-epoch'),
    path('forecast/add/', add_forecast, name='add-forecast'),
    path('transaction/add/', add_transaction, name='add-transaction'),
    path('forecast/save/', save_forecast, name='save-forecast'),
    path('transaction/save/', save_transaction, name='save-transaction'),
    path('epoch/mark-as-useful/<int:id>', mark_as_useful, name='mark-as-useful'),
    path('transaction/index/', index_transaction, name='index-transaction'),
    path('forecast/index', index_forecast, name='index-forecast'),
    path('forecast/<int:id>/edit/', edit_forecast, name='edit-forecast'),
    path('transaction/<int:id>/edit/', edit_transaction, name='edit-transaction')


]
