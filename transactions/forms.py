from django import forms
from transactions.models import MoneyTransaction, Deposit

# class TransactionForm(forms.ModelForm):
#     class Meta:
#         model = MoneyTransaction
#         fields = [
#             'amount'
#         ]

    # def __init__(self, *args, **kwargs):
    #     # self.account = kwargs.pop('account') # account value ke pop kore anlam
    #     # print(kwargs)
    #     super().__init__(*args, **kwargs)



class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['amount']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        min_deposit_amount = 100

        if amount is None:
            raise forms.ValidationError(
                f'invalid amount'
            )
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )
    
        return amount



    


