from django.test import TestCase
from results.models import *
# Create your tests here.


class StudentInfoTestCase(TestCase):
    def setup(self):
        StudentInfo.objects.create(std_name='asad',std_class=9, std_roll=1)
        


    def test_student(self):
        self.std=StudentInfo.objects.get(std_name='asad')
        self.assertEqual(self.std.std_name, 'asad')
