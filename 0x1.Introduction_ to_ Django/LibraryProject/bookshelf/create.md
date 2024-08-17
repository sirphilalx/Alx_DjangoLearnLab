# Creating a Book Instance

```
from bookshelf.models import Book


# Create a new Book instance with the specified attributes

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)


# Save the Book instance to the database
book.save()

# Print all Book instances to verify creation
print(Book.objects.all())
```
