from django.contrib import admin
from library.models import Category, Book, Borrow, Comment
# Register your models here.

class SelectCategory(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

admin.site.register(Category, SelectCategory)
admin.site.register(Book)
admin.site.register(Borrow)
admin.site.register(Comment)