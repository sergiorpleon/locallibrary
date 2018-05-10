from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance


"""    Admin Autor    """
class BooksInline(admin.TabularInline):
    model = Book
    
#admin.site.register(Author)
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'imagen_author', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', 'photo' , ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]
    
    def imagen_author(self, obj):
		return obj.imagen_tag()
    
    imagen_author.allow_tags = True


    
# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


"""    Admin Genre    """
admin.site.register(Genre)


"""    Admin Book    """
#admin.site.register(Book)
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


"""    Admin Book Instance    """  
#admin.site.register(BookInstance)
# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )