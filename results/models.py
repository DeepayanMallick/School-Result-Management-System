from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from .grade_sheet import SubjectGrade, SubjectGradePoint
from django.utils import timezone

from django.db.models import Avg, Count, Min, Sum


STD_CLASS = (
    ('6', 'Six'),
    ('7', 'Seven'),
    ('8', 'Eight'),
    ('9', 'Nine'),
    ('10', 'Ten'),
)


STD_GENDER = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
)

STD_GROUP = (
        ('S', 'Science'),
        ('B', 'Business Studies'),
        ('H', 'Humatics'),
        ('G', 'General')
)


REGULAR = 'R'
OPTIONAL = 'O'

SUBJECT_TYPE_CHOICE = (
        (REGULAR, 'REGULAR'),
        (OPTIONAL, 'OPTIONAL')
)






class CustomUser(AbstractUser):
    name=models.CharField('Full Name',max_length=100)



class StdCommon(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class SubjectTecher(StdCommon):
    teacher_name=models.CharField('Teacher Name', max_length=100)
    teach_phone_number=models.IntegerField('Mobile Number')
    teach_major_subject=models.CharField('Subject Name: ', max_length=100)


    def __str__(self):
        return self.teacher_name



class StdSubject(StdCommon):


    subject_name = models.CharField('Subject Name', max_length=100)
    teacher=models.ForeignKey(SubjectTecher, on_delete=models.CASCADE, related_name='teacher')
    subject_group = models.CharField(
        'Subject Group', choices=STD_GROUP, default='G', max_length=10)

    subject_code=models.CharField('Subject Code', max_length=10)
    subjet_class = models.CharField(
        'Subject Class', max_length=2, choices=STD_CLASS, default='6')
    subject_type = models.CharField(
        'Subject Type', max_length=1, default=REGULAR, choices=SUBJECT_TYPE_CHOICE)
    subject_full_marks = models.DecimalField(
        'Full Marks', max_digits=5, decimal_places=2, default=100,blank=True, null=True)



    subject_theory_full_marks = models.FloatField('Theory Marks', blank=True, null=True)
    subject_mcq_full_marks = models.FloatField('MCQ', blank=True, null=True)
    subject_practical_marks = models.FloatField('Practical', blank=True, null=True)
    subject_total_marks = models.FloatField('Total Marks', blank=True, null=True, help_text='Plz dont input any number')

    '''
        Bangla and English first 2nd part marks added
    '''

    first_part_name = models.CharField('First Subject Name', max_length=100, blank=True, null=True)
    first_part_theory_full_marks = models.FloatField('First Part Theory Marks', blank=True, null=True)
    first_part_mcq_full_marks = models.FloatField('First Part MCQ Marks', blank=True, null=True)

    second_part_name = models.CharField('Second Subject Name', max_length=100, blank=True, null=True)
    second_part_theory_full_marks = models.FloatField(
        'Second Part Theory Marks', blank=True, null=True)
    second_part_mcq_full_marks = models.FloatField('Second MCQ Marks', blank=True, null=True)


    first_second_full_marks = models.FloatField('1st and 2nd Part Total marks', blank=True, null=True)






    subject_form_searh_name=models.CharField('Subject Search Form name', max_length=500, blank=True, null=True)


    def __str__(self):
        return self.subject_name+' Class '+self.subjet_class+' '+' '+self.subject_type+' Code '+self.subject_code


    def save(self, *args, **kwargs):
        subject_form_searh_name=self.subject_name+' Class '+self.subjet_class+' '+' '+self.subject_type+' Code '+self.subject_code

        self.subject_form_searh_name=subject_form_searh_name


        try:
            self.subject_full_marks = self.subject_theory_full_marks
            theory_full=self.subject_theory_full_marks
        except:
            self.subject_full_marks = 0
            self.subject_theory_full_marks=None
            theory_full=0

        if self.subject_theory_full_marks == None:
            self.subject_theory_full_marks = None


        '''
        MCQ Marks added
        '''
        try:
            if self.subject_full_marks==None:
                self.subject_full_marks=0
            self.subject_full_marks = self.subject_full_marks + self.subject_mcq_full_marks
        except:
            if self.subject_full_marks==None:
                self.subject_full_marks=0
            self.subject_full_marks = self.subject_full_marks


        '''

        Practical Marks

        '''

        try:
            self.subject_full_marks = self.subject_full_marks + self.subject_practical_marks
        except:
            self.subject_full_marks = self.subject_full_marks

        self.subject_total_marks = self.subject_full_marks


        if self.subject_total_marks == None or self.subject_total_marks ==0:
            '''
            First and 2nd part adding marks

        '''
            try:
                self.first_second_full_marks=self.first_part_theory_full_marks
                try:
                    self.first_second_full_marks = self.first_second_full_marks+ self.first_part_mcq_full_marks
                except:
                    self.first_second_full_marks = self.first_second_full_marks
            except:
                self.first_second_full_marks = self.first_second_full_marks

            if self.first_second_full_marks != None:
                try:
                    self.first_second_full_marks = self.first_second_full_marks + self.second_part_theory_full_marks

                except:
                   self.first_second_full_marks = self.first_second_full_marks


                try:
                    self.first_second_full_marks = self.first_second_full_marks+ self.second_part_mcq_full_marks
                except:
                    self.first_second_full_marks = self.first_second_full_marks

                self.subject_total_marks = self.first_second_full_marks

            elif self.first_second_full_marks == None:
                self.first_second_full_marks == None

            self.subject_total_marks = self.subject_total_marks
            self.subject_full_marks=self.subject_total_marks



        super(StdSubject, self).save(*args, **kwargs) # Call the real save() method

    class Meta:
        verbose_name = ("Subject")
        verbose_name_plural = ("Subject")
        ordering = ['subject_code']

class StudentInfo(StdCommon):




    std_name = models.CharField('Student Name',max_length=100, help_text='Type only student Full Name like as Nazmul Islam or Nazrul Islam', blank=True, null=True)
    std_class = models.CharField('Student Class',max_length=2, choices=STD_CLASS, default=10, help_text='Select a class')
    std_roll = models.IntegerField('Roll Number',help_text='Type Student Roll Number (Only Number)')
    std_group=models.CharField('Group', choices=STD_GROUP, max_length=1, default='G')
    std_gender=models.CharField('Gender', max_length=10, choices=STD_GENDER, default='MALE')
    #std_subjects = models.ManyToManyField(StdSubject)


    std_total_marks = models.FloatField('Total Marks', default=0, blank=True, null=True)
    std_marks_with_fail_sub = models.FloatField(
        'Total Marks', default=0, blank=True, null=True)

    std_gpa = models.CharField('GPA', max_length=50,default='F', blank=True, null=True)

    std_grade_point_total_sum=models.FloatField('Total Avg Number per Subject', blank=True, null=True) # toal grade point sum

    std_grade_point_total_subject_avg = models.FloatField(
        'Total GPA', blank=True, null=True) #avg gradepoint

    std_fail_subject=models.IntegerField('Fail Subject', blank=True, null=True)


    school_rank=models.IntegerField('Student Rank in School',default=0, blank=True, null=True)
    class_rank = models.IntegerField(
        'Student Rank in Class', default=0, blank=True, null=True)



    def __str__(self):
        return self.std_name

    class Meta:
            verbose_name = ("Student Detail")
            verbose_name_plural = ("Student Detail's")
            ordering = ['std_roll']


    def total_marks_sum(self):
        std_id = self.id
        x = Marks.objects.filter(std_name=std_id).aggregate(
            total_number=Sum('subject_marks')).get('total_number', 0)

        return x


    def save(self, *args, **kwargs):

        std_id = self.id
        fail_sub = 0
        std_result='Pass'

        total_number = Marks.objects.filter(std_name=std_id).aggregate(
            total_number=Sum('subject_marks')).get('total_number', 0)
        self.std_marks_with_fail_sub = Marks.objects.filter(std_name=std_id).aggregate(
             total_number_f=Sum('subject_total_marks')).get('total_number_f', 0)

        subject_grade = ((Marks.objects.filter(std_name=std_id, subject_gradepoint__gte=1).aggregate(sp=Sum('subject_gradepoint')).get('sp', 0)))



        self.std_total_marks = total_number

        if subject_grade is None:
            subject_grade=0


        self.std_grade_point_total_sum = subject_grade

        subject_grade_f = Marks.objects.filter(std_name=std_id, subject_name__subject_type__startswith='R')
        absent_check_f = Marks.objects.filter(std_name=std_id)




        try:
            class_rank_new = Rank.objects.get(std=self.id)
            self.class_rank = class_rank_new.class_rank
            self.school_rank = class_rank_new.school_rank
        except :
            self.class_rank = 0
            self.school_rank = 0


        for i in subject_grade_f:

            if 'F' == i.subject_gpa:
                fail_sub = fail_sub+1

        if fail_sub >= 1:
            std_result = 'Fail ' +str(fail_sub)+' Subject'
            #self.std_gpa = std_result



        self.std_fail_subject=fail_sub

        if fail_sub >= 1:
            self.std_grade_point_total_subject_avg=0

        else:
            if self.std_class == '6' or self.std_class == '7':
                self.std_grade_point_total_subject_avg ='%2f' % (subject_grade/7)
            elif self.std_class == '8':
                self.std_grade_point_total_subject_avg ='%2f' % (subject_grade/7)

            elif self.std_class == '9' or self.std_class == '10':
                self.std_grade_point_total_subject_avg = '%2f' % (subject_grade/9)

        for i in absent_check_f:
            if i.absent_check == 'Y':
                self.std_grade_point_total_subject_avg = -100
                std_result = 'Withheld'
                break

        self.std_gpa = std_result

        super(StudentInfo, self).save(*args, **kwargs) # Call the real save() method










class Marks(StdCommon):
    std_name = models.ForeignKey(
        StudentInfo, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(StdSubject, on_delete=models.CASCADE)

    ABSENT=(
        ('N', 'No'),
        ('Y', 'Yes'),
    )

    absent_check=models.CharField(max_length=10, choices=ABSENT, default='N')


    subject_theory=models.FloatField('Theory', blank=True, null=True)
    subject_mcq = models.FloatField('MCQ', blank=True, null=True)
    subject_practical=models.FloatField('Practical', blank=True, null=True)


    first_part_theory = models.FloatField('1st Theory', blank=True, null=True)
    first_part_mcq = models.FloatField('1st MCQ', blank=True, null=True)
    second_part_theory = models.FloatField('2nd Theory', blank=True, null=True)
    second_part_mcq = models.FloatField('2nd MCQ', blank=True, null=True)

    subject_total_marks = models.FloatField('Total Marks', blank=True, null=True)
    subject_gpa_sub = models.CharField('Subject GPA Sub', max_length=5, blank=True, null=True, help_text="Please keep blank")


    subject_marks = models.DecimalField('Full Marks', max_digits=5,
    decimal_places=2, help_text='Please give proper number', blank=True,
    null=True)

    subject_gradepoint = models.DecimalField(
        'Grade Point', max_digits=3, decimal_places=1, blank=True, null=True, help_text="Please keep blank")
    subject_gpa = models.CharField('Subject GPA', max_length=5, blank=True, null=True, help_text="Please keep blank")



    '''
    def __str__(self):
        return self.std_name.std_name+' Class: '+str(self.std_name.std_class)+' Roll: '+str(self.std_name.std_roll) +' ' + self.subject_name.subject_name +' '+str(self.subject_marks)
    '''
    def __str__(self):
        return f'{self.subject_name.subject_name}  {self.subject_marks}, {self.subject_gradepoint}, {self.subject_gpa}'

    class Meta:
        verbose_name = ("Mark Details")
        verbose_name_plural = ("Result Sheet Details")
        ordering = ['subject_name']
        unique_together = (("std_name", "subject_name"),)

    def subject_grade(self):
        grade = SubjectGrade(self.subject_marks,self.subject_name.subject_full_marks).subgrade()
        return grade

    def subject_grade_point(self):
        grade = SubjectGradePoint( self.subject_marks, self.subject_name.subject_full_marks).subgrade()
        return grade


    def save(self, *args, **kwargs):



        '''
            Practical and MCQ number and grade point automatic add
        '''
        #subject_theory, subject_mcq, subject_practical,subject_total_marks
        #subject_name,subject_theory_full_marks,subject_mcq_full_marks, subject_practical_marks

        #if self.subject_name.subjet_class == '9' or self.subject_name.subjet_class == '10':




        if self.subject_name.subjet_class == '6' or self.subject_name.subjet_class == '7' or self.subject_name.subjet_class == '8' and (self.subject_name.first_part_theory_full_marks == None and self.subject_name.second_part_theory_full_marks == None and self.subject_name.first_part_mcq_full_marks == None and self.subject_name.second_part_mcq_full_marks == None):

            theory = 0
            mcq = 0
            practical = 0
            fail_sub_sub = ['Pass']

            if self.subject_name.subject_theory_full_marks != None:
                theory = self.subject_theory

            elif self.subject_name.subject_theory_full_marks == None:
                self.subject_theory = None

            if self.subject_name.subject_mcq_full_marks != None:
                mcq = self.subject_mcq
            elif self.subject_name.subject_mcq_full_marks == None:
                self.subject_mcq = None


            if self.subject_name.subject_practical_marks != None:
               practical = self.subject_practical

            elif self.subject_name.subject_practical_marks == None:
                self.subject_practical = None

            try:
                self.subject_total_marks = mcq+practical+theory
            except:
                if mcq == None:
                    mcq = 0
                elif practical == None:
                    practical = 0
                elif theory == None:
                    theory = 0

            try:
                self.subject_total_marks = mcq+practical+theory
            except:
                self.subject_total_marks = mcq+practical

            pass_marks = (self.subject_name.subject_total_marks/100)*33

            simple_fail=[]

            try:
                if self.subject_total_marks >= round(pass_marks+.1):
                    simple_fail.append('Pass')
                elif self.subject_total_marks < pass_marks:
                    simple_fail.append('F')

                self.subject_gpa_sub = 'Pass'
                for fail in simple_fail:
                    if fail == 'F':
                        self.subject_gpa_sub = 'F'
                        break

            #input number from subject total number
                if self.subject_gpa_sub == 'F':
                    self.subject_marks = 0
                else:
                    self.subject_marks = self.subject_total_marks

            except:
                #self.subject_total_marks=2
                self.subject_marks = self.subject_total_marks


        if self.subject_name.subjet_class == '9' or self.subject_name.subjet_class == '10' and (self.subject_name.first_part_theory_full_marks == None and self.subject_name.second_part_theory_full_marks == None and self.subject_name.first_part_mcq_full_marks == None and self.subject_name.second_part_mcq_full_marks == None):

            theory = 0
            mcq = 0
            practical = 0
            fail_sub_sub = ['Pass']

            if self.subject_name.subject_theory_full_marks != None:
                try:
                    theory = self.subject_theory

                except:
                    theory = 0

            elif self.subject_name.subject_theory_full_marks == None:
                self.subject_theory = None

            if self.subject_name.subject_mcq_full_marks != None:
                try:
                    mcq = self.subject_mcq
                except:
                    mcq = 0
            elif self.subject_name.subject_mcq_full_marks == None:
                self.subject_mcq = None

            if self.subject_name.subject_practical_marks != None:
                try:
                    practical = self.subject_practical
                except:
                    practical = 0
            elif self.subject_name.subject_practical_marks == None:
                self.subject_practical = None

            try:
                self.subject_total_marks = mcq+practical+theory
            except:
                if mcq == None:
                    mcq = 0
                elif practical == None:
                    practical = 0
                elif theory == None:
                    theory = 0

            self.subject_total_marks = mcq+practical+theory




            try:
                theory_pass_marks = (self.subject_name.subject_theory_full_marks/100)*33

                if self.subject_theory >= round(theory_pass_marks+.1):
                    fail_sub_sub.append('Pass')
                elif self.subject_theory < theory_pass_marks or self.subject_theory == 0:
                    fail_sub_sub.append('F')
            except:
                self.subject_theory = None

            try:
                mcq_pass_marks = (self.subject_name.subject_mcq_full_marks/100)*33

                if self.subject_mcq >= round(mcq_pass_marks+.1):
                    fail_sub_sub.append('Pass')
                elif self.subject_mcq < mcq_pass_marks or self.subject_mcq == 0:
                    fail_sub_sub.append('F')
            except:
                self.subject_mcq = None

            try:
                practical_pass_marks = (
                    self.subject_name.subject_practical_marks/100)*33
                if self.subject_practical >= round(practical_pass_marks+.1):
                    fail_sub_sub.append('Pass')
                elif self.subject_practical >= practical_pass_marks or self.subject_practical == 0:
                    fail_sub_sub.append('F')
            except:
                self.subject_practical = None

            self.subject_gpa_sub = 'Pass'
            for fail in fail_sub_sub:
                if fail == 'F':
                    self.subject_gpa_sub = 'F'
                    break

            #input number from subject total number
            if self.subject_gpa_sub == 'F':
                self.subject_marks = 0
            else:
                self.subject_marks = self.subject_total_marks


        '''
            Bangla and English for six to ten
        '''

        if self.subject_name.first_part_theory_full_marks != None and (self.subject_name.subjet_class == '9' or self.subject_name.subjet_class == '10'):

            if self.subject_name.first_part_theory_full_marks != None and self.subject_name.second_part_theory_full_marks != None and self.subject_name.first_part_mcq_full_marks != None and self.subject_name.second_part_mcq_full_marks != None:

                try:
                    total_theory_q_marks=self.subject_name.first_part_theory_full_marks + self.subject_name.second_part_theory_full_marks
                    total_theory = self.first_part_theory + self.second_part_theory

                except:
                    total_theory = 0
                    #total_theory_q_marks = 0
                    pass

                try:
                    total_mcq_q_marks = self.subject_name.first_part_mcq_full_marks + self.subject_name.second_part_mcq_full_marks
                    total_mcq = self.first_part_mcq + self.second_part_mcq
                except:
                    total_mcq = 10
                    #total_mcq_q_marks = 0
                    pass


                pass_fail=[]

                thoery_pass_marks=(total_theory_q_marks/100)*33
                mcq_pass_marks = (total_mcq_q_marks/100)*33

                if total_theory >= round(thoery_pass_marks+.1):
                    pass_fail.append('Pass')

                elif total_theory < round(thoery_pass_marks+.1):
                    pass_fail.append('F')

                if total_mcq >= round(mcq_pass_marks+.1):
                    pass_fail.append('Pass')
                elif total_mcq < round(mcq_pass_marks+.1):
                    pass_fail.append('F')

                self.subject_total_marks = total_theory + total_mcq

                self.subject_gpa_sub = 'Pass'

                for i in pass_fail:
                    if i == 'F':
                        self.subject_gpa_sub = 'F'
                        break

                if self.subject_gpa_sub == 'F':
                    self.subject_marks = 0
                else:
                    self.subject_marks = self.subject_total_marks


            elif self.subject_name.first_part_theory_full_marks != None and self.subject_name.second_part_theory_full_marks != None:
                try:
                    total_theory_q_marks = self.subject_name.first_part_theory_full_marks + self.subject_name.second_part_theory_full_marks
                    total_theory = self.first_part_theory + self.second_part_theory

                except:
                    total_theory = 0
                    total_theory_q_marks = 0



                pass_fail = []

                thoery_pass_marks = (total_theory_q_marks/100)*33


                if total_theory >= round(thoery_pass_marks+.1):
                    pass_fail.append('Pass')
                elif total_theory < round(thoery_pass_marks+.1):
                    pass_fail.append('F')



                self.subject_total_marks = total_theory

                self.subject_gpa_sub = 'Pass'

                for i in pass_fail:
                    if i == 'F':
                        self.subject_gpa_sub = 'F'
                        break

                if self.subject_gpa_sub == 'F':
                    self.subject_marks = 0
                else:
                    self.subject_marks = self.subject_total_marks

        if self.subject_name.first_part_theory_full_marks!= None and (self.subject_name.subjet_class == '6' or self.subject_name.subjet_class == '7' or self.subject_name.subjet_class == '8'):

                if self.subject_name.first_part_theory_full_marks != None:
                    theory_one = self.first_part_theory
                    fist_theory_q_marks=self.subject_name.first_part_theory_full_marks
                else:
                    theory_one = 0
                    fist_theory_q_marks=0


                if self.subject_name.second_part_theory_full_marks != None:
                    theory_two =  self.second_part_theory
                    second_theory_marks=self.subject_name.second_part_theory_full_marks
                else:
                    theory_two=0
                    second_theory_marks = 0


                if self.subject_name.first_part_mcq_full_marks != None:
                    mcq_one=self.first_part_mcq
                    first_mcq_q_marks=self.subject_name.first_part_mcq_full_marks
                else:
                    mcq_one=0
                    first_mcq_q_marks=0

                if self.subject_name.second_part_mcq_full_marks != None:
                    mcq_two=self.second_part_mcq
                    mcq_tow_q_marks=self.subject_name.second_part_mcq_full_marks
                else:
                    mcq_two=0
                    mcq_tow_q_marks=0

                question_marks = fist_theory_q_marks + second_theory_marks+first_mcq_q_marks+mcq_tow_q_marks
                total_marks_sum = theory_one+theory_two+mcq_one+mcq_two

                pass_fail = []

                thoery_pass_marks = (question_marks/100)*33

                if total_marks_sum >= round(thoery_pass_marks+.1):
                    pass_fail.append('Pass')
                elif total_marks_sum < round(thoery_pass_marks+.1):
                    pass_fail.append('F')


                self.subject_total_marks = total_marks_sum

                self.subject_gpa_sub = 'Pass'

                for i in pass_fail:
                    if i == 'F':
                        self.subject_gpa_sub = 'F'
                        break

                if self.subject_gpa_sub == 'F':
                    self.subject_marks = 0
                else:
                    self.subject_marks = self.subject_total_marks














        if self.subject_name.subject_theory_full_marks == None:
            self.subject_theory = None

        if self.subject_name.subject_mcq_full_marks == None:
            self.subject_mcq = None

        if self.subject_name.subject_practical_marks == None:
            self.subject_practical = None







        if self.subject_name.first_part_theory_full_marks != None and self.subject_name.first_part_name != None:
            part_fail_subject = []
            first_mcq_part1 = 0
            first_theory_part = 0
            second_mcq_part = 0
            second_theory_part = 0






        if self.subject_name.first_part_theory_full_marks == None:
            self.first_part_theory=None

        if self.subject_name.first_part_mcq_full_marks == None:

            self.first_part_mcq = None

        if self.subject_name.second_part_theory_full_marks == None:

            self.second_part_theory = None


        if self.subject_name.second_part_mcq_full_marks == None:

           self.second_part_mcq = None



        if self.absent_check == 'Y':
            self.subject_marks=0




        grade_point = SubjectGradePoint(
            self.subject_marks, self.subject_name.subject_full_marks).subgrade()
        gpa = SubjectGrade(self.subject_marks,
                           self.subject_name.subject_full_marks).subgrade()

        if self.subject_name.subject_type == 'O':

            if self.subject_marks >= ((self.subject_name.subject_full_marks/100)*50) and self.subject_marks <= self.subject_name.subject_full_marks:
                subject_opt_grade_point = grade_point-2

                self.subject_gradepoint = subject_opt_grade_point
                self.subject_gpa = gpa

            elif self.subject_marks >= ((self.subject_name.subject_full_marks/100)*33) and self.subject_marks < ((self.subject_name.subject_full_marks/100)*50):
                self.subject_gradepoint = 0
                self.subject_gpa = gpa

            elif self.subject_marks < ((self.subject_name.subject_full_marks/100)*33):
                self.subject_gradepoint = 0
                self.subject_gpa = gpa

        elif self.subject_name.subject_type == 'R':
            self.subject_gradepoint = grade_point
            self.subject_gpa = gpa


        super().save(*args, **kwargs)





class Rank(models.Model):
    std = models.ForeignKey(StudentInfo, related_name='std', on_delete=models.CASCADE)

    total_marks = models.DecimalField(
        max_digits=5, decimal_places=2, help_text='Please give proper number', default=0, blank=True, null=True)
    total_gpa = models.DecimalField(
        max_digits=5, decimal_places=2, help_text='Please give proper number', default=0, blank=True, null=True)
    class_rank = models.IntegerField(default=0, blank=True, null=True)
    school_rank=models.IntegerField('All School Rank', default=0, blank=True, null=True)



    def __str__(self):
        return 'Name: %s |  Marks: %s | Class Rank %s | School Rank %s' % (self.std, self.total_marks, self.class_rank, self.school_rank)

    class Meta:
            verbose_name = ("Rank")
            verbose_name_plural = ("Rank")
            ordering = ['class_rank']
