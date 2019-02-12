from django.contrib import admin

from results.models import StudentInfo, StdSubject, Marks, Rank, SubjectTecher

from django.urls import resolve
from django.db.models import Q

class RankInstanceInline(admin.TabularInline):
    model=Rank
    fk_name='std'
    extra=0


STD_CLASS = (
    ('6', 'Six'),
    ('7', 'Seven'),
    ('8', 'Eight'),
    ('9', 'Nine'),
    ('10', 'Ten'),
)


class SubjectInstanceInline(admin.TabularInline):
    model = Marks
    fk_name = 'std_name'
    extra = 1

    exclude = ['subject_gradepoint', 'subject_gpa','subject_gpa_sub', 'subject_marks', 'subject_total_marks']

    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        '''resolved = resolve(request.path_info)
        if resolved.args:
            return self.parent_model.objects.get(pk=resolved.args[0])
        return None
        '''

        resolved = resolve(request.path_info)
        if resolved.kwargs.get('object_id'):

            x=self.parent_model.objects.get(pk=resolved.kwargs['object_id'])
            return x



    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        parent = self.get_parent_object_from_request(request)
        get_parent=parent.std_class
        get_group=parent.std_group
        if db_field.name == "subject_name":
            kwargs["queryset"] =  StdSubject.objects.filter(Q(subjet_class__exact=get_parent), Q(subject_group__exact=get_group)| Q(subject_group__exact='G'))


        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        parent = self.get_parent_object_from_request(request)

        get_parent=int(parent.std_class)
        if get_parent>=6 and get_parent <= 8:
            self.max_num = 7
        if get_parent >= 9 and get_parent <= 10:
            self.max_num=10
        return super().get_formset(request, obj, **kwargs)



class SubjectInstance(admin.StackedInline):
    model = StdSubject
    fk_name = 'teacher'
    extra = 8

    exclude = ['subject_form_searh_name',
               'subject_full_marks', 'subject_total_marks', 'first_second_full_marks']





@admin.register(StudentInfo)
class StudentAdmin(admin.ModelAdmin):
    list_filter = ('std_class', 'std_gender', 'std_group')
    list_display = ('std_name', 'std_class', 'std_group', 'std_gender', 'std_roll')
    inlines = [SubjectInstanceInline]


    search_fields = ('std_name','std_roll','std_group')


    exclude = ['std_total_marks', 'std_gpa','std_grade_point_total_sum','std_marks_with_fail_sub', 'std_grade_point_total_subject_avg', 'std_fail_subject','school_rank','class_rank']









@admin.register(StdSubject)
class SubjectModelAdmin(admin.ModelAdmin):
    list_filter = ('subjet_class', 'subject_type')
    list_display = ('subject_name', 'subjet_class',
                    'subject_type', 'subject_full_marks')

    search_fields = ('subject_name', 'subject_code')










@admin.register(SubjectTecher)
class SubjectTecherModel(admin.ModelAdmin):
    list_filter = ('teacher_name','teach_phone_number')
    search_fields = ('teacher_name', 'teach_phone_number')

    inlines = [SubjectInstance]

