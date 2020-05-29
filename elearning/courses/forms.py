from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module, Test

ModuleFormSet = inlineformset_factory(Course,
                                    Module,
                                    fields=['title', 'description','learning_style'],
                                    extra=2,
                                    can_delete=True)

labels = {'title': 'Tytuł testu', 'description': 'Opis', 'rating_weight': 'Waga oceny(0-100)'}

TestFormSet = inlineformset_factory(Course,
                                    Test,
                                    fields=['title', 'description','rating_weight' ],
                                    extra=1,
                                    labels=labels,
                                    can_delete=True)