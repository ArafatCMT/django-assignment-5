from django.shortcuts import render,redirect
from django.views.generic import DetailView
from library.models import Book,Borrow
from django.contrib.auth.mixins import LoginRequiredMixin
from library.forms import CommentForm
from authors.models import Registration
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.
class BookDetailView(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'
    context_object_name = 'book'


class BookDetailViewForUnloggedinUser(BookDetailView):

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        book = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.save()
            return self.get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        comments = book.comments.all()
        context['comments'] = comments
        
        return context


class BookDetailViewForloggedinUser( LoginRequiredMixin,BookDetailView):

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        book = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.save()
            return self.get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        comments = book.comments.all()
        comment_form = CommentForm()
        borrow = Borrow.objects.filter(userId=self.request.user.id)
        # print(self.request.user, self.request.user.account.balance)
        # user er balance
        balance = self.request.user.account.balance

        borrow_bookId = []
        for pair in borrow:
            # print(pair.bookId, pair.userId)
            borrow_bookId.append(pair.bookId)

        context['comments'] = comments
        context['comment_form'] = comment_form
        context['borrow_bookId'] = borrow_bookId
        context['balance'] = balance

        return context


def BookBorrowView(request, id):
    # print('hello')
    book = Book.objects.get(id=id)
    # print(book.borrow_price)

    user = Registration.objects.get(user=request.user)
    # print(user, user.balance)
    user.balance -= book.borrow_price
    user.save(update_fields=['balance'])
    
    borrow = Borrow.objects.create(bookId=id, userId=request.user.id)
    borrow.save()

    email_subject = "Borrowing Book Message"
    message = render_to_string('borrowing_mail.html',{
        'user': user,
        'book': book,
    })
    to_email = request.user.email
    email = EmailMultiAlternatives(email_subject, '', to=[to_email])
    email.attach_alternative(message, 'text/html')
    email.send()

    # return redirect('book_details', id)
    return redirect('book_details_for_loggedin_user', id)
        
