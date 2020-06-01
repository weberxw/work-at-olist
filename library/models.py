from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=150)

class Book(models.Model):
    name = models.CharField(max_length=150)
    publication_year = models.PositiveSmallIntegerField()
    edition = models.CharField(max_length=150)
    authors = models.ManyToManyField(Author)
