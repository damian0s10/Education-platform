from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    path('register/',
        views.StudentRegistrationView.as_view(),
        name='student_registration'),
    path('profile/',
        views.ProfileView.as_view(),
        name='profile'),
    path('profile/update/',
        views.ProfileUpdateView.as_view(),
        name='profile_update'),
    path('profile/password/',
        views.ChangePasswordView.as_view(),
        name='change-password'),
    path('enroll-course/',
        views.StudentEnrollCourseView.as_view(),
        name='student_enroll_course'),
    path('courses/',
        views.StudentCourseListView.as_view(),
        name='student_course_list'),
    path('course/<pk>/',
        views.StudentCourseDetailView.as_view(),
        name='student_course_detail'),
    path('course/<pk>/<module_id>/',
        views.StudentCourseDetailView.as_view(),
        name='student_course_detail_module'),

    path('tests/<course_id>/',
        views.StudentCourseTestsView.as_view(),
        name='student_course_tests'),
    path('tests/solve/<test_id>/',
        views.StudentTestView.as_view(),
        name='student_test_view'),

    path('grades/<course_id>/',
        views.StudentGradesView.as_view(),
        name='student_course_grades'),
    
]
