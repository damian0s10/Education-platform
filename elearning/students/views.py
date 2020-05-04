from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login
from braces.views import LoginRequiredMixin
from .forms import ( 
    CourseEnrollForm, 
    UserCreateForm, 
    UpdateProfileForm, 
    UpdateLearningStyle
)
from django.views.generic.list import ListView
from courses.models import Course, UserProfile
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from django.shortcuts import redirect


class StudentRegistrationView(CreateView):
    template_name='students/student/registration.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('student_course_list')
   
    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        profile = UserProfile(user=user)
        profile.save()
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm
    
    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('student_course_detail', args=[self.course.id])

class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = None
        return context
    

class ProfileView(LoginRequiredMixin, TemplateResponseMixin,View):
    template_name = 'students/student/profile.html'
    
    def get(self, request, *args, **kwargs):
        formset = UpdateLearningStyle(instance=request.user.profile)
        return self.render_to_response({'user': request.user,
                                        'formset': formset})
    def post(self, request, *args, **kwargs):
        formset = UpdateLearningStyle(request.POST, instance=request.user.profile)
        if formset.is_valid():
            formset.save()
            return redirect('profile')
        return self.render_to_response({'user': request.user,
                                        'formset': formset})
    
class ProfileUpdateView(LoginRequiredMixin, TemplateResponseMixin,View):
    template_name = 'students/student/update_profile.html'

    def get(self, request, *args, **kwargs):
        formset = UpdateProfileForm(instance=request.user)
        return self.render_to_response({'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = UpdateProfileForm(request.POST, instance=request.user)
        if formset.is_valid():
            formset.save()
            return redirect('profile_update')
        return self.render_to_response({'formset': formset})

class ChangePasswordView(LoginRequiredMixin, TemplateResponseMixin,View):
    template_name = 'students/student/change_password.html'

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user)
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        return self.render_to_response({'form': form})