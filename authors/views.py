from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login
from authors.forms import RegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from library.models import Borrow, Book
from authors.models import Registration
from transactions.models import MoneyTransaction


# Create your views here.
class RegistrationFormView(FormView):
    template_name = 'authors/register_form.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'authors/login_form.html'
    
    def get_success_url(self):
        return reverse_lazy('profile')
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
class UserLogoutView(LogoutView):
    def get_redirect_url(self):
        return reverse_lazy('login')

@login_required
def profile(request):
    borrow = Borrow.objects.filter(userId=request.user.id)
    transaction_id =  request.user.id

    books = []
    for obj in borrow:
        # print(pair.bookId, pair.userId, pair.is_borrowed)
        book = Book.objects.get(id=obj.bookId)
        books.append((book,obj.is_borrowed))
    
    return render(request, 'authors/profile.html', {'books': books, 'transaction_id': transaction_id})

def UpdateBalanceView(request, book_id):
    user = Registration.objects.get(user=request.user)
    book = Book.objects.get(id=book_id)
    # print(user.balance, book.title, book.borrow_price)
    user.balance += book.borrow_price
    user.save(update_fields=['balance'])

    borrow = Borrow.objects.filter(userId=request.user.id)
    for obj in borrow:
        if book.id == obj.bookId:
            obj.is_borrowed = False
            # print('ok done')
            obj.save(update_fields=['is_borrowed'])
            break

    return redirect('profile')


