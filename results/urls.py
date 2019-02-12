from .views import Homepage
from django.urls import path,re_path
from django.conf import settings



from .views import StudentDetails, StudentAdd, ResultUpdate, StudentUpdateView, StudentAddmarks, student_add_marks, Pdf, SubjectSeaechView, SubjectDetailView, AllRankViewSearch, TeacherAllView, TeacherDetailView,SummaryView
urlpatterns = [
    path('', Homepage.as_view(), name='home'),

    path('subject-search/', SubjectSeaechView.as_view(), name='subject_search'),

    path('class_wise_rank_search/', AllRankViewSearch.as_view(
        template_name='results/all_rank_search.html'), name='all_rank_search'),

    re_path(r'^(?P<pk>\d+)/subject-detail/$', SubjectDetailView.as_view(), name='subject_details'),

    re_path(r'^(?P<pk>\d+)/student-result-details/$', StudentDetails.as_view(), name='std_details'),

    path('student_add/', StudentAdd.as_view(), name='std_add'),
    re_path(r'student_update/(?P<pk>\d+)/$', StudentUpdateView.as_view(), name='std_update'),

    re_path(r'student_marks_add/(?P<pk>\d+)/$', StudentAddmarks.as_view(), name='std_add_marks'),


    re_path(r"std_add_marks_func/(?P<pk>\d+)/$", student_add_marks, name='stdAdd_marks'),

    re_path(r"std_marks_update/(?P<pk>\d+)/$",ResultUpdate.as_view(), name='stdmarks_update'),

    re_path(r'^(?P<pk>\d+)/get-print-result-sheet/',Pdf.as_view(), name='pdf'),

    path('teacher_list/', TeacherAllView.as_view(), name='teacher_list'),

    re_path(r'^(?P<pk>\d+)/teachers-profile/', TeacherDetailView.as_view(), name='teacher_detail'),

    path('summary/', SummaryView.as_view(), name='summary'),
    

    
]



