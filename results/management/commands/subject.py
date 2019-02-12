from django.core.management.base import BaseCommand, CommandError
from results.models import StudentInfo, Marks, StdSubject as Subject, Rank
import random


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for poll_id in options['poll_id']:

            try:

                poll = Subject.objects.filter(subject_type=poll_id)

            except Subject.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            for x in poll:
                x.opened = False
                x.save()

            self.stdout.write(self.style.SUCCESS(
                'Successfully closed Subject update "%s"' % poll_id))
