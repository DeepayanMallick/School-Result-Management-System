


class SubjectGrade:

    def __init__(self, subject_number, subject_full_number):
        self.subject_number = subject_number
        self.subject_full_number = subject_full_number

    def subgrade(self):
        number_aplus = (self.subject_full_number/100)*80
        number_a = (self.subject_full_number/100)*70
        number_aminus = (self.subject_full_number/100)*60
        number_b = (self.subject_full_number/100)*50
        number_c = (self.subject_full_number/100)*40
        number_d = (self.subject_full_number/100)*33
        number_f = (self.subject_full_number/100)*1

        if self.subject_number >= number_aplus and self.subject_number:
            return 'A+'
        elif self.subject_number >= number_a and self.subject_number < (number_aplus):
            return 'A'

        elif self.subject_number >= number_aminus and self.subject_number <(number_a):
            return 'A-'

        elif self.subject_number >= number_b and self.subject_number <(number_aminus):
            return 'B'

        elif self.subject_number >= number_c and self.subject_number <(number_b):
            return 'C'

        elif self.subject_number >= number_d and self.subject_number <(number_c):
            return 'D'

        elif self.subject_number >= number_f and self.subject_number <(number_d):
            return 'F'

        elif self.subject_number == 0:
            return 'F'
        

class SubjectGradePoint:

    def __init__(self, subject_number, subject_full_number):
        self.subject_number = subject_number
        self.subject_full_number = subject_full_number

    def subgrade(self):
        number_aplus = (self.subject_full_number/100)*80
        number_a = (self.subject_full_number/100)*70
        number_aminus = (self.subject_full_number/100)*60
        number_b = (self.subject_full_number/100)*50
        number_c = (self.subject_full_number/100)*40
        number_d = (self.subject_full_number/100)*33
        number_f = (self.subject_full_number/100)*1

        if self.subject_number >= number_aplus and self.subject_number:
            return 5
        elif self.subject_number >= number_a and self.subject_number < (number_aplus):
            return 4

        elif self.subject_number >= number_aminus and  self.subject_number < (number_a):
            return 3.5

        elif self.subject_number >= number_b and self.subject_number < (number_aminus):
            return 3

        elif self.subject_number >= number_c and self.subject_number < (number_b):
            return 2

        elif self.subject_number >= number_d and self.subject_number < (number_c):
            return 1

        elif self.subject_number >= number_f and self.subject_number < (number_d):
            return 0

        elif self.subject_number==0:
            return 0
