from django.urls import path
from .views import github

urlpatterns = [
    path('getdata/', github.as_view(), name='getalldata'),
]
