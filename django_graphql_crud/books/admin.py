from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year_published', 'isbn', 'created_by', 'created_at')
    list_filter = ('author', 'year_published')
    search_fields = ('title', 'author', 'isbn')