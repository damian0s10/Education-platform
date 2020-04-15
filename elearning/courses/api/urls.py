from django.urls import path
from . import views
from rest_framework import routers
from . import views
from django.conf.urls import include

app_name = 'api'
router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)

urlpatterns = [
    path('subjects/',
        views.SubjectListView.as_view(),
        name='subject_list'),
    path('subjects/<pk>/',
        views.SubjectDetailView.as_view(),
        name='subject_detail'),
    path('', include(router.urls)),
]