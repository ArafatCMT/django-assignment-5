from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField(upload_to='book_img')
    borrow_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    borrow_date = models.DateField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'
    

class Borrow(models.Model):
    bookId = models.IntegerField()
    userId = models.IntegerField()
    is_borrowed = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return f'Book id {self.bookId} borrow by User id {self.userId} '
    
class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'comment by {self.name}'

