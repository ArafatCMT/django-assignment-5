from django.shortcuts import render,redirect
from transactions.forms import DepositForm
from transactions.models import MoneyTransaction
from authors.models import Registration
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def DepositMoneyView(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = Registration.objects.get(user=request.user)
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data.get('amount')
                print(user.balance)

                user.balance += amount

                user.save(
                    update_fields = ['balance']
                )

                MoneyTransaction.objects.create(account=user, amount=amount)

                email_subject = "Deposit Message"
                message = render_to_string('deposit_mail.html',{
                    'user': request.user,
                    'amount': amount,
                })
                to_email = request.user.email
                email = EmailMultiAlternatives(email_subject, '', to=[to_email])
                email.attach_alternative(message, 'text/html')
                email.send()

                return redirect('deposit')
        else:
            form = DepositForm()
        return render(request, 'deposit_form.html', {'form': form})
    else:
        return redirect('login')
