from django.urls import path
from .views import DepositMoneyView
urlpatterns = [
    path('deposit/', DepositMoneyView, name='deposit'),
]