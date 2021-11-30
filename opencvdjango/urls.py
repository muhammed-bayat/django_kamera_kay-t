from django.urls import path

from core import settings
from opencvdjango import views

urlpatterns = [
    path('', views.home, name='home_page'),
    path('webcam_feed', views.webcam_feed, name='webcam_feed'),
    path('upload/', views.upload_file),

 ]