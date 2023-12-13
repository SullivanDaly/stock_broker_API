from django.core.management.base import BaseCommand, CommandError
from ...db_scripts import populate

class Command(BaseCommand):
    help = 'Populates database with random data'

    def handle(self, *args, **options):
        populate()
        self.stdout.write(self.style.SUCCESS('Successfully populated database'))