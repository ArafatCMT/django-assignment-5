from django.db import models
from authors.models import Registration

class MoneyTransaction(models.Model):
    account = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.account.user.id}'
    

class Deposit(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    

