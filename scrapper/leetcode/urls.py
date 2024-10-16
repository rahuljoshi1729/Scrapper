from .views import *
from django.urls import path

urlpatterns = [
    path('userprofile/',userprofile.as_view(),name='fecth user profile'),

]