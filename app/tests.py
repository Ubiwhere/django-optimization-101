from rest_framework.test import APITestCase
from django.db import connection, reset_queries
from django.conf import settings
from .factories import BookFactory


class BookTestCase(APITestCase):
    def create_object(self):
        return BookFactory.create()

    def test_nplusone_queries(self):
        """Ensures that the API view is not suffering from N+1 queries
        problem."""

        # Replace with your endpoint, possibly using `reverse`
        endpoint: str = (
            "/api/ex3/queryset-optimization/select-related/without-optimization/"
        )
        # Turn on debug so we can record the queries
        settings.DEBUG = True

        # Create initial object and reset queries
        self.create_object()
        reset_queries()
        self.assertEqual(len(connection.queries), 0)

        # Make first request and save number of queries
        self.client.get(endpoint)
        count1 = len(connection.queries)
        self.assertNotEqual(count1, 0)

        # Create another object and reset queries
        self.create_object()
        reset_queries()

        self.assertEqual(len(connection.queries), 0)

        # Make another api request and get new number of queries
        self.client.get(endpoint)
        count2 = len(connection.queries)
        self.assertNotEqual(count2, 0)

        # Set debug to false again
        settings.DEBUG = False

        # Ensure that the query count has not increased
        self.assertEqual(
            count1,
            count2,
            msg=f"N+1 queries problem detected at endpoint {endpoint}",
        )
