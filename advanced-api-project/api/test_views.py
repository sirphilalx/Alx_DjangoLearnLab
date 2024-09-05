from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create an author
        self.author = Author.objects.create(name='Test Author')

        # Create a book
        self.book = Book.objects.create(title='Test Book', publication_year=2022, author=self.author)

    def test_create_book(self):
        """Test creating a new book"""
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)  # Check if the book count increased
        self.assertEqual(Book.objects.get(id=2).title, 'New Book')  # Verify the book data

    def test_get_book_list(self):
        """Test retrieving the list of books"""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return 1 book

    def test_update_book(self):
        """Test updating an existing book"""
        url = reverse('book-update', args=[self.book.id])
        data = {
            'title': 'Updated Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()  # Refresh the book instance from the database
        self.assertEqual(self.book.title, 'Updated Book')  # Verify the updated title

    def test_delete_book(self):
        """Test deleting a book"""
        url = reverse('book-delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)  # Ensure the book was deleted

    def test_filter_books(self):
        """Test filtering books by title"""
        url = reverse('book-list') + '?search=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return the test book

    def test_order_books(self):
        """Test ordering books by publication year"""
        url = reverse('book-list') + '?ordering=publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the books are ordered correctly (only one book in this case)

    def test_permission_required(self):
        """Test that unauthenticated users cannot create a book"""
        self.client.logout()  # Log out the test user
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Should be forbidden
