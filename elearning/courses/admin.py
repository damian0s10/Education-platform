from django.contrib import admin
from .models import Subject, Course, Module, UserProfile, Test, Question, QuestionClosed, ShortAnswer, Grade
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin) 

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title','slug']
    prepopulated_fields = {'slug': ('title',)}

class ModuleInLine(admin.StackedInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_field = {'slug': ('title',)}
    inlines = [ModuleInLine]

class QuestionClosedInLine(admin.StackedInline):
    model = QuestionClosed

class ShortAnswerInLine(admin.StackedInline):
    model = ShortAnswer

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    inlines = [QuestionClosedInLine, ShortAnswerInLine]

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['test', 'student', 'grade']
    

# @admin.register(QuestionClosed)
# class QuestionClosedAdmin(admin.ModelAdmin):
#     list_display = [f.name for f in QuestionClosed._meta.fields]