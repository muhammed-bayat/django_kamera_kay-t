from django.urls import path
from .views import *

from apps.opencvdjango import views

app_name = 'opencvdjango'

urlpatterns = [
    path('', index, name='index'),
    path('upload/', views.upload_file),
]
