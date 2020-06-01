from django.http import HttpResponse
from rest_framework import generics
from rest_framework import permissions
from library.models import Author, Book
from library.serializers import BookSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 20
    
class AuthorsList(generics.ListAPIView):
    """
        Get a paginated list of all Authors or filtered by name
    """
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Author.objects.all()
    pagination_class = DefaultPagination


    def get_queryset(self):
        queryset = self.queryset.all().order_by('name')
        q = self.request.query_params.get('q')
        if q is not None:
            queryset = queryset.filter(name__icontains=q)
        return queryset

    def get(self, request):
        authors_list = []
        for q in self.get_queryset():
            json = {}
            json['id'] = q.id
            json['name'] = q.name
            authors_list.append(json)

        page = self.paginate_queryset(authors_list)
        return self.get_paginated_response(page)

class Books(generics.RetrieveUpdateDestroyAPIView):
    """
        Add, edit, delete and get specific Book, or get all books. 
    """
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = self.queryset.all()
        name = self.request.query_params.get('name', None)
        year = self.request.query_params.get('year', None)
        edition = self.request.query_params.get('edition', None)
        author = self.request.query_params.get('author', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        if year is not None:
            queryset = queryset.filter(publication_year=year)
        if edition is not None:
            queryset = queryset.filter(edition__icontains=edition)
        if author is not None:
            queryset = queryset.filter(authors__name__icontains=author)
        return queryset

    def get(self, request, pk=None):
        try:
            queryset = self.get_queryset()
            if pk is not None:
                queryset = self.queryset.filter(id=pk)
        except:
            return Response("Book not found", status=404)

        page = self.paginate_queryset(queryset.order_by('name'))
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)
        
    def post(self, request):
        data = request.data
        name = data.get('name', None)
        edition = data.get('edition', None)
        publication_year = data.get('publication_year', None)
        authors = Author.objects.filter(id__in=data.get('authors', []))

        if not (name and edition and publication_year and authors):
            return Response("Invalid input.", status=400)

        new_book = Book.objects.create(name=name, edition=edition, publication_year=publication_year)
        new_book.authors.set(authors)

        serializer = self.serializer_class(new_book, many=False)
        return Response(serializer.data, status=200)
    
    def patch(self, request, pk):
        try:
            data = request.data
            book = Book.objects.get(id=pk)
        except:
            return Response("Book not found.", status=404)
            
        name = data.get('name', None)
        edition = data.get('edition', None)
        publication_year = data.get('publication_year', None)
        authors = Author.objects.filter(id__in=data.get('authors', []))

        if name:
            book.name = name
        if edition:
            book.edition = edition
        if publication_year:
            book.publication_year = publication_year
        if authors:
            book.authors.clear()
            book.authors.set(authors)
        book.save()

        serializer = self.serializer_class(book, many=False)
        return Response(serializer.data, status=200)
    
    def delete(self, request, pk):
        try:
            data = request.data
            book = Book.objects.get(id=pk)
        except:
            return Response("Book not found.", status=404)
            
        book.delete()
        return Response("Book deleted.", status=200)