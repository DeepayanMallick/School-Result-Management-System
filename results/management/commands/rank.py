from django.core.management.base import BaseCommand, CommandError
from results.models import StudentInfo, Marks, StdSubject as Subject, Rank
import random


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for poll_id in options['poll_id']:
            std_count = StudentInfo.objects.filter(std_class=poll_id).count()
            std_count_all_class = StudentInfo.objects.all().count()

            for std_order in StudentInfo.objects.filter(std_class=poll_id).order_by('std_grade_point_total_subject_avg', 'std_total_marks','-std_roll'):
                try:
                    rank = Rank.objects.get(std=std_order)
                except Rank.DoesNotExist:
                    rank = Rank(std=std_order)
                rank.total_marks = std_order.std_total_marks
                rank.total_gpa = std_order.std_grade_point_total_subject_avg
                rank.class_rank = std_count

                rank.save()
                std_count = std_count-1

            for std_order in StudentInfo.objects.order_by('std_grade_point_total_subject_avg', 'std_total_marks','-std_roll'):
                try:
                    rank = Rank.objects.get(std=std_order)
                except Rank.DoesNotExist:
                    rank = Rank(std=std_order)
                rank.total_marks = std_order.std_total_marks
                rank.total_gpa = std_order.std_grade_point_total_subject_avg
                rank.school_rank = std_count_all_class
                rank.save()
                std_count_all_class = std_count_all_class-1

            self.stdout.write(self.style.SUCCESS(
                    'Successfully closed ranks "%s"' % poll_id))
