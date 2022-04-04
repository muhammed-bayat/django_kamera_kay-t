from django.urls import path
from .views import *

from apps.opencvdjango import views
app_name = 'opencvdjango'

urlpatterns = [
    path('', index, name='index'),
    path('test', quiz, name='quiz'),
    # path('webcam_feed', views.webcam_feed, name='webcam_feed'),
    path('upload/', views.upload_file),

 ]