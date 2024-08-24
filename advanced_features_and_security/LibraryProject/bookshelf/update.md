# Updating the book instance

```
from bookshelf.models import Book

# Retrieve the Book instance with the title "1984"
book = Book.objects.get(title="1984")

# Update the title of the Book instance
book.title = "Nineteen Eighty-Four"

# Save the changes to the database
book.save()

# Verify that the title has been updated
updated_book = Book.objects.get(title="Nineteen Eighty-Four")
print(f"Updated Title: {updated_book.title}")
```
