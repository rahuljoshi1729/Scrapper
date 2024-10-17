from django.urls import path
from .views import codeforces

urlpatterns = [
    path('getdata/', codeforces.as_view(), name='getalldata'),
]
