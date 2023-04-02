"""
Contains model fake data factories
"""

import factory
import factory.fuzzy
from faker import Faker

from app.models import Book, Author, Country
import random
from django.utils.translation import gettext_lazy as _

fake = Faker()


class CountryFactory(factory.django.DjangoModelFactory):
    """Builds a `Country` with dummy data."""

    name = factory.Faker("country")
    continent = factory.LazyAttribute(
        lambda x: fake.random_element(
            elements=(
                _("Asia"),
                _("Africa"),
                _("North America"),
                _("South America"),
                _("Antarctica"),
                _("Europe"),
                _("Australia"),
            )
        )
    )

    class Meta:
        model = Country


class AuthorFactory(factory.django.DjangoModelFactory):
    """Builds a `Author` with dummy data."""

    name = factory.Faker("name")
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = Author


class BookFactory(factory.django.DjangoModelFactory):
    """Builds a `Book` with dummy data."""

    title = factory.Faker("text")
    isbn = factory.Faker("isbn10")
    author = factory.SubFactory(AuthorFactory)
    publisher = factory.Faker("text")

    class Meta:
        model = Book


def generate_mock_data():
    """Generates random authors and random books associated with the authors"""
    authors = AuthorFactory.create_batch(5000)
    for _ in range(20000):
        BookFactory(author=random.choice(authors))
