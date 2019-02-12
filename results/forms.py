from django import forms
from .models import StudentInfo, Marks, StdSubject
from django.forms import inlineformset_factory

class ProfileSearchForm(forms.Form):
    std_class = forms.CharField(required=False)




class AddStudentInfo(forms.ModelForm):
    class Meta:
        model=StudentInfo
        fields=("__all__")



class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model=StudentInfo

        fields=("__all__")

    
class StudentSubjectGPAForm(forms.ModelForm):
    class Meta:
        model = Marks

        exclude = ('std_name', 'subject_gpa',
                   'subject_gradepoint', 'std_result')

    
class StudentSubjectGPAFormAdd(forms.ModelForm):
    class Meta:
        model = Marks
        exclude = ('std_name','subject_gpa',
                   'subject_gradepoint', 'std_result')

    def __init__(self, *args, **kwargs):
        super(StudentSubjectGPAFormAdd, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['subject_marks'].queryset = StudentInfo.objects.filter(
                std_name__exact=self.instance.id)


class Addmarks(forms.Form):
   #students = forms.ModelChoiceField(queryset=StudentInfo.objects.get(pk=27))
   subject = forms.ModelChoiceField(queryset=StdSubject.objects.all())
   marks = forms.IntegerField()





''

class ResultSearchForm(forms.Form):
    STD_CLASS = (
        ('6', 'Six'),
        ('7', 'Seven'),
        ('8', 'Eight'),
        ('9', 'Nine'),
        ('10', 'Ten'),
    )

    std_roll_form = forms.IntegerField(label="Roll Number",min_value=1, max_value=99)
    std_class_form = forms.ChoiceField(choices=STD_CLASS, label="Select Class")







class SubjectSearchForm(forms.Form):
    STD_CLASS = (
        ('6', 'Six'),
        ('7', 'Seven'),
        ('8', 'Eight'),
        ('9', 'Nine'),
        ('10', 'Ten'),
    )
    subject_name=forms.ModelChoiceField(queryset=StdSubject.objects.all(), label='Select Subject Name', empty_label=None)
    subject_class = forms.ChoiceField(choices=STD_CLASS, label="Select Class")


class ClassSearchForm(forms.Form):
    STD_CLASS = (
        ('6', 'Six'),
        ('7', 'Seven'),
        ('8', 'Eight'),
        ('9', 'Nine'),
        ('10', 'Ten'),
    )

    student_class = forms.ChoiceField(choices=STD_CLASS, label="Select Class")
