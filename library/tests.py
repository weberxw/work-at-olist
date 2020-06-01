from django.test import TestCase
from library.models import Author, Book
from library.views import AuthorsList, Books
import json
from rest_framework.test import APIRequestFactory


class LibraryTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        a_author = Author.objects.create(name='J. K. Rowling')
        b_author = Author.objects.create(name='Paulo Coelho')
        c_author = Author.objects.create(name='Stephen King')
        d_author = Author.objects.create(name='Clarice Lispector')
        e_author = Author.objects.create(name='George R. R. Martin')

        a_book = Book.objects.create(name='Book AAA', publication_year=2015, edition='Edition one')
        b_book = Book.objects.create(name='Book BBB', publication_year=2015, edition='Edition two')
        c_book = Book.objects.create(name='Book CCC', publication_year=2017, edition='Edition three')
        d_book = Book.objects.create(name='Book DDD', publication_year=2018, edition='Edition four')

        a_book.authors.set([a_author])
        b_book.authors.set([b_author, c_author])
        c_book.authors.set([d_author])
        d_book.authors.set([a_author])
    
    def test_AuthorsView(self):
        view = AuthorsList.as_view()
        request = self.factory.get('/authors/', content_type='application/json')        
        response = view(request) 
        resp = response.data.get('results', [])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 5)
        self.assertIn('J. K. Rowling', str(resp))
        self.assertIn('Paulo Coelho', str(resp))
        self.assertIn('Stephen King', str(resp))
        self.assertIn('Clarice Lispector', str(resp))
        self.assertIn('George R. R. Martin', str(resp))

    def test_BooksGetAll(self):
        view = Books.as_view()
        request = self.factory.get('/books/', content_type='application/json')        
        response = view(request) 
        resp = response.data.get('results', [])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 4)
        self.assertIn('Book AAA', str(resp))
        self.assertIn('Book BBB', str(resp))
        self.assertIn('Book CCC', str(resp))
        self.assertIn('Book DDD', str(resp))

    def test_BooksGetSpecific(self):
        request = self.factory.get('/books/', content_type='application/json')        
        response = Books.as_view()(request, pk=1)
        resp = response.data.get('results', [])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 1)
        self.assertIn('Book AAA', str(resp))
        self.assertIn('Edition one', str(resp))
        self.assertIn('2015', str(resp))
        self.assertIn('J. K. Rowling', str(resp))

    def test_BooksGetFilteredByName(self):
        request = self.factory.get('/books/?name=Book BBB', content_type='application/json')        
        view = Books.as_view()
        response = view(request)
        resp = response.data.get('results', [])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 1)
        self.assertIn('Book BBB', str(resp))
        self.assertIn('Edition two', str(resp))
        self.assertIn('2015', str(resp))
        self.assertIn('Paulo Coelho', str(resp))
        self.assertIn('Stephen King', str(resp))
    
    def test_BooksGetFilteredByYear(self):
        request = self.factory.get('/books/?year=2015', content_type='application/json')        
        view = Books.as_view()
        response = view(request)
        resp = response.data.get('results', [])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 2)

    def test_BooksGetFilteredByAuthor(self):
        request = self.factory.get('/books/?author=Clarice Lispector', content_type='application/json')        
        view = Books.as_view()
        response = view(request)
        resp = response.data.get('results', [])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 1)
        self.assertIn('Book CCC', str(resp))
        self.assertIn('Edition three', str(resp))
        self.assertIn('2017', str(resp))
        self.assertIn('Clarice Lispector', str(resp))


    def test_AddNewBook(self):
        data = {
                'name': "A song of ice and fire",
                'publication_year': "2015",
                'edition': 'First Edition',
                'authors': [5]
                }

        view = Books.as_view()
        request = self.factory.post('/books/', content_type='application/json', data=json.dumps(data)) 
        response = view(request) 
        resp = response.data


        self.assertEqual(response.status_code, 200)
        self.assertIn('A song of ice and fire', str(resp))
        self.assertIn('First Edition', str(resp))
        self.assertIn('2015', str(resp))
        self.assertIn('George R. R. Martin', str(resp))
    
    def test_EditBook(self):
        data = {
                'name': "New edited name",
                'publication_year': "1991",
                'edition': 'Second Edition',
                'authors': [4]
                }

        request = self.factory.patch('/books/', content_type='application/json', data=json.dumps(data))        
        response = Books.as_view()(request, pk=1)
        resp = response.data


        self.assertEqual(response.status_code, 200)
        self.assertIn('New edited name', str(resp))
        self.assertIn('Second Edition', str(resp))
        self.assertIn('1991', str(resp))
        self.assertIn('Clarice Lispector', str(resp))
    
    def test_DeleteBook(self):
        request = self.factory.delete('/books/', content_type='application/json')        
        response = Books.as_view()(request, pk=1)
        resp = response.data


        self.assertEqual(response.status_code, 200)
        self.assertIn('Book deleted.', str(resp))