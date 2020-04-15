from django.urls import path
from . import views

urlpatterns = [
    path('test/',
         views.PersonalityTest.as_view(),
         name='personality_test'),

]
