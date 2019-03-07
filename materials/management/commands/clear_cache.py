from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):

    def handle(self, *args, **options):
        cache._cache.flush_all()
        self.stdout.write("Successfully clear cache")
