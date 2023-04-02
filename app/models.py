from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)
    continent = models.CharField(max_length=100)


class Author(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)
    publisher = models.CharField(max_length=255)
