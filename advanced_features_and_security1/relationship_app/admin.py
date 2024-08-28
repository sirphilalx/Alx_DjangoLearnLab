from django.contrib import admin
from .models import Author, Book, Library, Librarian
from django.contrib.auth.admin import UserAdmin
from .models import User

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Librarian, LibrarianAdmin)
admin.site.register(User, CustomUserAdmin)