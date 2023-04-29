from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
import re
from heart_data import views
print('dats------')
urlpatterns = [
    url(r'python/data', views.DataReader.as_view(), name="dataReader")
]
