from django import template
from results.models import StudentInfo, StdSubject, SubjectTecher


@register.simple_tag
def get_total_taka(teacher_id):

    teacher_id.stdsubject_set.all().aggregate(Max(''))

    return sum([each.customer_due for each in customer_info_object.stdsubject_set.all()])
