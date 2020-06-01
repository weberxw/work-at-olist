
# Olist backend test by Lucas Weber

### Description
This is an API for a library to store book and authors data.

For demonstration purposes all user authentication and specific permissions verification has been disabled, so you can access all endpoints without login in.


### Dependencies
* python3.6
* asgiref==3.2.7
* dj-database-url==0.5.0
* Django==3.0.6
* django-heroku==0.3.1
* djangorestframework==3.11.0
* gunicorn==20.0.4
* pkg-resources==0.0.0
* psycopg2==2.8.5
* psycopg2-binary==2.8.5
* pytz==2020.1
* sqlparse==0.3.1
* whitenoise==5.1.0


### Import data
To read the authors csv you just need to call **python manage.py csv_reader --path 'path_to_csv'**

After that the API will import all Authors to the database taking care to not allow duplicate names


### Services

* **GET https://olistapi.herokuapp.com/library/authors/** - Get a paginated list of Authors

* **GET https://olistapi.herokuapp.com/library/authors/?q=name** - Get authors filtered by full name or part of it
	 
     ex. https://olistapi.herokuapp.com/library/authors/?q=George R. R. Martin

* **POST https://olistapi.herokuapp.com/library/books/** - Add a new book

Body:

{
    "name": "This is a test book",
    "edition": "First Edition",
    "publication_year": 2015,
    "authors": [1,2]
}

* **PATCH https://olistapi.herokuapp.com/library/books/{ID}/** - Update an existent book by ID

Body:

{
    "name": "This name was edited",
    "edition": "Second Edition",
    "publication_year": 2015,
    "authors": [3]
}

* **DELETE https://olistapi.herokuapp.com/library/books/{ID}/** - Delete an existent book by ID

* **GET https://olistapi.herokuapp.com/library/books/** - Get a paginated list of Books

* **GET https://olistapi.herokuapp.com/library/books/{ID}/** - get a specific book by ID
	
    ex. https://olistapi.herokuapp.com/library/books/12/  

* **GET https://olistapi.herokuapp.com/library/books/?name='name'** - get a list of books filtered by name
	
    ex. https://olistapi.herokuapp.com/library/books/?name='The song of ice and fire'

* **GET https://olistapi.herokuapp.com/library/books/?year=YEAR** - get a list of books filtered by publication year
	
    ex. https://olistapi.herokuapp.com/library/books/?year=2015  

* **GET https://olistapi.herokuapp.com/library/books/?edition='edition'** - get a list of books filtered by edition
	
    ex. https://olistapi.herokuapp.com/library/books/?edition="First Edition"

* **GET https://olistapi.herokuapp.com/library/books/?author='name'** - get a list of books filtered by author's name
	
    ex. https://olistapi.herokuapp.com/library/books/?author="George R. R. Martin"
  
**Note:** You can use a composition of this four filters too using the & character, for example:
	
ex. https://olistapi.herokuapp.com/library/books/?author="George R. R. Martin"&year=2015


### Testing

For testing you just need to call **python manage.py test --keepdb library.tests**

The *keepdb* flag preserves the test database between test runs. Increasing the speed to run the tests.

If all went well all tests must have passed.

### Environment

This code was developed on a Intel® Core™ i5-7300HQ CPU @ 2.50GHz × 4, 16GB RAM

OS: Linux - Ubuntu 18.04.3 LTS

All python libs were installed inside a virtualenv


#### If you have any problems or doubts executing this, please call me!

#### weberxw@gmail.com
