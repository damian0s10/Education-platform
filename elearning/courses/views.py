from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Module, Content, Subject, Test, Question, Grade
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet, TestFormSet
from django.forms.models import modelform_factory
from django.apps import apps
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from django.views.generic.detail import DetailView
from students.forms import CourseEnrollForm
from django.contrib import messages
from django.contrib.auth.models import User
from itertools import chain
from operator import attrgetter

class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'

class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except:
            return render(request, template_name=self.template_name, context=self.get_context_data())
        

class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'

class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request,pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                            instance=self.obj,
                            data=request.POST,
                            files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})

class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})

class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})

class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'
    

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(total_courses=Count('courses'))
        courses = Course.objects.annotate(total_modules=Count('modules'))

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course':self.object}) 
        return context
    
class CourseStudentsListView(PermissionRequiredMixin, ListView):
    model = User
    template_name = 'courses/course/students.html'
    permission_required = 'courses.change_course'
    course = None

    def get_queryset(self):
        self.course = get_object_or_404(Course, pk=self.kwargs['pk'])
        if self.course.owner == self.request.user:
            qs = super().get_queryset()
            return qs.filter(course_joined__in=[self.kwargs['pk']])
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['course'] = self.course
        return data

    
        
class CourseTestUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/test/formset.html'
    permission_required = 'courses.change_course'
    course = None
    students = None

    def get_formset(self, data=None):
        return TestFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        self.students = self.course.students.all()       
        return super().dispatch(request,pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            obj = formset.save()
            if obj:
                for student in self.students:
                    g = Grade(test=obj[-1],student=student)
                    g.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

class TestManageView(TemplateResponseMixin, View):
    template_name = 'courses/manage/test/manage.html'
    permission_required = 'courses.change_course'
    course = None
    tests = None

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        self.tests = self.course.tests.all()       
        return super().dispatch(request,pk)
    
    def get(self,request, *args, **kwargs):
        return self.render_to_response({'course': self.course,
                                        'tests': self.tests})


class QuestionCreateUpdateView(TemplateResponseMixin, View):
    test = None
    model = None
    obj = None
    template_name = 'courses/manage/test/create.html'
    permission_required = 'courses.change_course'

    def get_model(self, question_type):
        if question_type in ['questionclosed', 'shortanswer']:
            return apps.get_model(app_label='courses',
                                model_name=question_type)
        return None

    def get_form(self, model, *args, **kwargs):
        labels = {'title': 'Tytuł','order': 'Kolejność:','answers_a':'Odp a',
                  'answers_b':'Odp b', 'answers_c':'Odp c', 'answers_d':'Odp d',
                  'correct_answer':'Poprawna odpowiedź','points': 'Punkty'}
        Form = modelform_factory(model, labels=labels, exclude=['test','question_type','answer'])
        return Form(*args, **kwargs)

    def dispatch(self, request, test_id, question_type, id=None):
        self.test = get_object_or_404(Test, id=test_id)
        self.model = self.get_model(question_type)
        if id:
            self.obj = get_object_or_404(self.model, id=id)
        return super().dispatch(request, test_id, question_type)

    def get(self, request, test_id, question_type):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, test_id, model_name, id=None):
        form = self.get_form(self.model,
                            instance=self.obj,
                            data=request.POST,
                            )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.test = self.test
            obj.save()
            return redirect('test_question_update', self.test.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})



class QuestionDeleteView(View):
    permission_required = 'courses.change_course'

    def get_model(self, question_type):
        if question_type in ['questionclosed', 'shortanswer']:
            return apps.get_model(app_label='courses',
                                model_name=question_type)
        return None
    def get(self, request, test_id, question_type,id):
        model = self.get_model(question_type)
        question = get_object_or_404(model, id = id)
        question.delete()
        return redirect('test_question_update', test_id)

class QuestionManageView(TemplateResponseMixin, View):
    test = None
    template_name = 'courses/manage/test/questions/manage.html'
    permission_required = 'courses.change_course'

    def dispatch(self, request, test_id):
        self.test = get_object_or_404(Test, id=test_id)
        return super().dispatch(request, test_id)

    def get(self, request, test_id):
        questions1 = self.test.questionclosed_set.all()
        questions2 = self.test.shortanswer_set.all()
        questions = sorted(
            chain(questions1, questions2),
            key=attrgetter('order'))
        return self.render_to_response({'questions': questions,
                                        'test': self.test})

class TeacherStudentGradesView(LoginRequiredMixin, TemplateResponseMixin,View):
    template_name = 'courses/course/grades.html'
    permission_required = 'courses.change_course'

    def get(self, request, course_id, student_id):
        grades = []
        course = get_object_or_404(Course, id=course_id)
        tests = course.tests.all()
        overall_rating = 0
        total_weight = 0
        for test in tests:
            grade = []
            grade.append(test.title)
            grade.append(test.rating_weight)
            
            student = get_object_or_404(User,id=student_id)
            g = get_object_or_404(Grade,test=test,student=student)
            
            if g.grade != None:
                grade.append(g.grade)
                grade.append(g.total)
                percent = round((g.grade/g.total)* 100,2) 
                grade.append(percent)
                grades.append(grade)
                overall_rating += percent * test.rating_weight
                total_weight += test.rating_weight
            else:
                grade.append(None)
                grades.append(grade)
                
        if total_weight:
            overall = round(overall_rating/total_weight,2)
        else:
            overall = 0
        return self.render_to_response({'grades': grades,
                                        'overall': overall})