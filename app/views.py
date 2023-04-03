from core.utils import time_response
from rest_framework.response import Response
from django.db.models import Q
from .models import Book, Author
from rest_framework import viewsets, mixins
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    CountrySerializer,
    AuthorWithCountrySerializer,
)
from rest_framework.decorators import action
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import Prefetch
from .factories import fake


class Ex1Viewset(viewsets.GenericViewSet):
    """Example view to demonstrate the differences between using
    low-level database operations vs python high-level ones."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @time_response
    @action(
        methods=["get"],
        url_path="filter-at-python",
        detail=False,
    )
    def filter_at_python(self, request, *args, **kwargs):
        """This API endpoint filters the books on which the
        title starts with the letter A."""
        filtered_books = []
        for book in Book.objects.all():
            if book.title.startswith("A"):
                filtered_books.append(book)

        serializer = BookSerializer(filtered_books, many=True)
        return Response(serializer.data)

    @time_response
    @action(
        methods=["get"],
        url_path="filter-at-database",
        detail=False,
    )
    def filter_at_database(self, request, *args, **kwargs):
        """This API endpoint filters the queryset using database
        queries."""
        filtered_books = Book.objects.filter(Q(title__startswith="A"))
        serializer = BookSerializer(filtered_books, many=True)
        return Response(serializer.data)

    @time_response
    @action(
        methods=["get"],
        url_path="non-optimized-create",
        detail=False,
    )
    def non_optimized_create(self, request, *args, **kwargs):
        """This API endpoint creates 10k books for the first author."""
        author = Author.objects.first()
        for _ in range(10000):
            Book.objects.create(title=fake.text(), isbn=fake.isbn10(), author=author)

        return Response()

    @time_response
    @action(
        methods=["get"],
        url_path="optimized-create",
        detail=False,
    )
    def optimized_create(self, request, *args, **kwargs):
        """This API endpoint creates 10k books for the first author, using
        an optimized operation"""
        author = Author.objects.first()
        books = []
        for _ in range(10000):
            books.append(Book(title=fake.text(), isbn=fake.isbn10(), author=author))

        Book.objects.bulk_create(books)

        return Response()


class Ex2Viewset(viewsets.GenericViewSet):
    """Example view to demonstrate queryset optimization using prefetch techniques."""

    queryset = Author.objects.all()

    class Ex2Serializer(serializers.ModelSerializer):
        """Serializer class for `Author` objects that includes a nested
        list representation of the authors' books."""

        books = BookSerializer(many=True, source="book_set")

        class Meta:
            model = Author
            fields = "__all__"

    serializer_class = Ex2Serializer

    @time_response
    @action(
        methods=["get"],
        url_path="without-optimization",
        detail=False,
    )
    def without_optimization(self, request, *args, **kwargs):
        """This API fetches the authors and their books without any
        optimization."""
        queryset = Author.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @time_response
    @action(
        methods=["get"],
        url_path="with-optimization",
        detail=False,
    )
    def with_optimization(self, request, *args, **kwargs):
        """This API fetches the authors and their books with
        optimization."""
        queryset = Author.objects.prefetch_related("book_set")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class Ex3Viewset(viewsets.GenericViewSet):
    """Example view to demonstrate queryset optimization of a foreign key using
    `select_related`."""

    queryset = Book.objects.all()

    class Ex3Serializer(serializers.ModelSerializer):
        """Serializer class for `Book` object that includes a nested
        representation of the associated `Author`."""

        author = AuthorWithCountrySerializer()

        class Meta:
            model = Book
            fields = "__all__"

    serializer_class = Ex3Serializer

    @time_response
    @action(
        methods=["get"],
        url_path="without-optimization",
        detail=False,
    )
    def without_optimization(self, request, *args, **kwargs):
        """This API fetches the books without any optimization."""
        queryset = Book.objects.all()[:10000]
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @time_response
    @action(
        methods=["get"],
        url_path="with-optimization",
        detail=False,
    )
    def with_optimization(self, request, *args, **kwargs):
        """This API fetches the books with a pre-fetch of the authors
        foreign keys."""
        queryset = Book.objects.select_related("author__country")[:10000]
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class Ex4Viewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Example view to demonstrate a more advanced pre-fetch optimization usage."""

    queryset = Author.objects.prefetch_related(
        Prefetch(
            "book_set",
            queryset=Book.objects.order_by("-date_published"),
            to_attr="cached_books",
        )
    )

    class Ex4Serializer(serializers.ModelSerializer):
        """Serializer class for `Author` that includes a nested JSON representation
        of a random book they have written."""

        last_book = serializers.SerializerMethodField()

        def get_last_book(self, obj: Author):
            if obj.cached_books:
                return BookSerializer(obj.cached_books[0]).data

        class Meta:
            model = Author
            fields = "__all__"

    serializer_class = Ex4Serializer

    # Override `list` to wrap-it in `time_response`
    @time_response
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class Ex5Viewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    """API endpoint to demonstrate the usage of cache."""

    queryset = Book.objects.select_related("author__country").order_by("-id")[:100]

    class Ex5Serializer(serializers.ModelSerializer):
        author = AuthorWithCountrySerializer()

        class Meta:
            model = Book
            fields = "__all__"

    serializer_class = Ex5Serializer

    @time_response
    @method_decorator(cache_page(15 * 60, key_prefix="books"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
