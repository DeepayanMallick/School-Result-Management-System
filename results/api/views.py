from .serializers import StudentSerializers
from results.models import StudentInfo
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAdminUser



class UserViewSet(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = StudentInfo.objects.all().order_by('-std_grade_point_total_subject_avg','std_roll')
    serializer_class = StudentSerializers
    #permission_classes = (IsAdminUser,)
