from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question
from courses.models import UserProfile
from django.http import HttpResponse

class PersonalityTest(TemplateResponseMixin, LoginRequiredMixin, View):
    template_name = 'test/test.html'
  
    def get(self, request, *args, **kwargs):
        questions = Question.objects.all()
        return self.render_to_response({'question_list': questions})

    def post(self, request, *args, **kwargs):
        a = 0
        b = 0
        c = 0
        d = 0

        for key, value in request.POST.items():
            if value == 'a': a += 1
            elif value == 'b': b += 1
            elif value == 'c': c += 1
            elif value == 'd': d += 1
        suma = a + b + c + d
        profile = UserProfile.objects.get(user=request.user.id)

        if max(a, b , c, d) == a: profile.learning_style = 'wzrokowiec'
        elif max(a, b , c, d) == b: profile.learning_style = 'słuchowiec'
        elif max(a, b , c, d) == c: profile.learning_style = 'dotykowiec'
        elif max(a, b , c, d) == d: profile.learning_style = 'kinestetyk'

        profile.save()
    
        return self.render_to_response({'a': round(a/suma * 100, 1),
                                        'b': round(b/suma * 100, 1),
                                        'c': round(c/suma * 100, 1),
                                        'd': round(d/suma * 100, 1),})