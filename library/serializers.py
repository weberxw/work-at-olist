from rest_framework import serializers
from library.models import Book, Author


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'name','edition', 'publication_year','authors']

    def get_authors(self, obj):
        authors = []
        for at in obj.authors.all():
            json = {}
            json['id'] = at.id
            json['name'] = at.name
            authors.append(json)
        return authors