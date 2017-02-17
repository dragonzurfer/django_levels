from django.core.management.base import BaseCommand
from brain.models import Moderator
from django.utils import timezone
class Command(BaseCommand):

    help = 'Expires event objects which are out-of-date'

    def handle(self, *args, **options):
        print Moderator.objects.filter(contest__end__lt=timezone.now()).delete()