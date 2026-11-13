import os
from django.core.management.base import BaseCommand, CommandError
from nano.DCv3.bot import NanoDC

class Command(BaseCommand):
    help = "Start NanoDCv3."
    def handle(mew, *args, **options):
        token = os.getenv("DISCORDKEY")
        if not token:
            raise CommandError("DISCORDKEY isn't set in .env!")

        nano = NanoDC("Bravely Daughter!")
        nano.run(token)