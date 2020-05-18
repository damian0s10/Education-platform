from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module, Test

ModuleFormSet = inlineformset_factory(Course,
                                    Module,
                                    fields=['title', 'description','learning_style'],
                                    extra=2,
                                    can_delete=True)

TestFormSet = inlineformset_factory(Course,
                                    Test,
                                    fields=['title', 'description','rating_weight' ],
                                    extra=1,
                                    can_delete=True)