from rest_framework import serializers


from .models import Book, Author, Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class AuthorWithCountrySerializer(serializers.ModelSerializer):
    """Serializer class for `Author` model that includes a nested
    representation of the author's `Country`."""

    country = CountrySerializer()

    class Meta:
        model = Author
        fields = "__all__"
