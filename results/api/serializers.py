from rest_framework import serializers
from results.models import StudentInfo, Marks, Rank, StdSubject


class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model=StudentInfo
        fields = ('id','std_name', 'std_gender', 'std_roll', 'std_class',
                  'get_std_group_display', 'std_grade_point_total_subject_avg', 'std_total_marks','std_gpa' )


