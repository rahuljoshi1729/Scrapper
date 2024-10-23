from django.urls import path
from .views import codechef

urlpatterns = [
    path('getdata/<str:username>', codechef.as_view(), name='codechef'),
]