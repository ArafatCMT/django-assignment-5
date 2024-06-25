from django.shortcuts import render
from library.models import Book, Category

def HomeView(request, slug=None):
    books = Book.objects.all()
    categories = Category.objects.all()
    
    if slug is not None:
        category = Category.objects.get(slug=slug)
        books = Book.objects.filter(category=category)
    
    return render(request, 'index.html', {'books': books, 'categories': categories})
