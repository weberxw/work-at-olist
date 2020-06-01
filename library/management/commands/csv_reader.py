import csv
from django.core.management import BaseCommand
from library.models import Author

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        filename = kwargs['path']
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            result = []
            for row in reader:
                try:
                    author,created = Author.objects.get_or_create(name=dict(row).get('name'))
                    print('Author: ' + author.name + ' - New on database: ' + str(created))
                except:
                    pass
                