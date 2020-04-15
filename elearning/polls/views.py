from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View
from .models import Question
from django.http import HttpResponse

class PersonalityTest(TemplateResponseMixin, View):
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
        sum = a + b + c + d

        return self.render_to_response({'a': round(a/sum* 100, 1),
                                        'b': round(b/sum* 100, 1),
                                        'c': round(c/sum* 100, 1),
                                        'd': round(d/sum* 100, 1),})