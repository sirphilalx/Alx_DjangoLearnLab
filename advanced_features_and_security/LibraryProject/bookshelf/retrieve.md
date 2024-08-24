# Retrieve the attributes of the class

```
from bookshelf.models import Book

# Retrieve the Book instance with title "1984"


book = Book.objects.get(title="1984")


# Display all attributes of the Book instance

print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```
