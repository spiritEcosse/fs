from materials.tasks import parser_premiere


class Command(BaseCommand):

    def handle(self, *args, **options):
        parser_premiere()
