from django.core.management.base import NoArgsCommand
from django.core.management import call_command


class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        call_command("loaddata", "packages")
