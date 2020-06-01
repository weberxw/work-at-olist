from django.conf.urls import url
from library import views

urlpatterns = [
    url(r'authors/', views.AuthorsList.as_view()),
    url(r'books/(?P<pk>[0-9]+)/', views.Books.as_view()),
    url(r'books/', views.Books.as_view()),
    
]
