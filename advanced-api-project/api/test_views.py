from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from api.models import Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        # Authenticated client
        self.client = APIClient()
        self.client.login(username="testuser", password="testpass123")

        # Book instances for filtering & searching tests
        self.book1 = Book.objects.create(
            title="Django Mastery",
            author="John Doe",
            publication_year=2020
        )
        self.book2 = Book.objects.create(
            title="Advanced Django REST",
            author="Jane Smith",
            publication_year=2023
        )
        self.book3 = Book.objects.create(
            title="Python Programming",
            author="John Doe",
            publication_year=2018
        )

        self.list_url = reverse("book-list")
        # book-detail is the name you assigned in urls.py
        self.detail_url = lambda pk: reverse("book-detail", args=[pk])

    # -------------------------
    #      CRUD TESTS
    # -------------------------

    def test_create_book_authenticated(self):
        data = {
            "title": "New Book",
            "author": "Alice Writer",
            "publication_year": 2024
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data["title"], "New Book")

    def test_create_book_unauthenticated(self):
        client = APIClient()
        data = {
            "title": "Unauthorized Create",
            "author": "No Auth",
            "publication_year": 2020
        }
        response = client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book(self):
        data = {"title": "Updated Title"}
        response = self.client.patch(
            self.detail_url(self.book1.id),
            data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book(self):
        response = self.client.delete(self.detail_url(self.book2.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    # -------------------------
    #   FILTERING TESTS
    # -------------------------

    def test_filter_books_by_author(self):
        response = self.client.get(f"{self.list_url}?author=John Doe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # book1 & book3

    def test_filter_books_by_year(self):
        response = self.client.get(f"{self.list_url}?publication_year=2023")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Advanced Django REST")

    # -------------------------
    #   SEARCH TESTS
    # -------------------------

    def test_search_books(self):
        response = self.client.get(f"{self.list_url}?search=Django")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data]
        self.assertIn("Django Mastery", titles)
        self.assertIn("Advanced Django REST", titles)

    # -------------------------
    #   ORDERING TESTS
    # -------------------------

    def test_order_books_by_title(self):
        response = self.client.get(f"{self.list_url}?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_order_books_by_publication_year_desc(self):
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
