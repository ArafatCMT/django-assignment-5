from django.urls import path
from library.views import BookDetailView, BookBorrowView, BookDetailViewForloggedinUser, BookDetailViewForUnloggedinUser

urlpatterns = [
   # path('detail/<int:id>', BookDetailView.as_view(), name='book_details'),
   path('book_detail/<int:id>', BookDetailViewForloggedinUser.as_view(), name='book_details_for_loggedin_user'),
   path('detail/<int:id>', BookDetailViewForUnloggedinUser.as_view(), name='book_details_for_unloggedin_user'),
   path('borrow/<int:id>', BookBorrowView, name='borrow_book'),
]