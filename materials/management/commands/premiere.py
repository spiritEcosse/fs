from materials.tasks import parser_premiere
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        parser_premiere()
