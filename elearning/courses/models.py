from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.utils.text import slugify
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):
    LEARNING_STYLES = (
        ('wzrokowiec', 'wzrokowiec'),
        ('słuchowiec', 'słuchowiec'),
        ('dotykowiec', 'dotykowiec'),
        ('kinestetyk', 'kinestetyk'),
    )
    user = models.OneToOneField(User, related_name='profile',  on_delete = models.CASCADE)
    learning_style = models.CharField(max_length=10, choices=LEARNING_STYLES, null=True, blank=True)

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    

class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name='course_joined', blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Module(models.Model):
    LEARNING_STYLES = (
        ('wzrokowiec', 'wzrokowiec'),
        ('słuchowiec', 'słuchowiec'),
        ('dotykowiec', 'dotykowiec'),
        ('kinestetyk', 'kinestetyk'),
        ('wszyscy', 'wszyscy'),
    )
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    learning_style = models.CharField(max_length=10, choices=LEARNING_STYLES)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)
    
class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, 
                                    on_delete=models.CASCADE, 
                                    limit_choices_to={'model__in':('text',
                                                                    'video',
                                                                    'image',
                                                                    'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=250,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name), {'item': self})
    
class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()

class Test(models.Model):
    course = models.ForeignKey(Course, related_name='tests', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # active_from = models.DateTimeField(blank=True)
    # active_time = models.DateTimeField(blank=True)
    rating_weight = models.IntegerField(default=1,
                                        validators=[MaxValueValidator(100), MinValueValidator(1)])
    
                                                                
class Question(models.Model):
    title = models.CharField(max_length=250)
    order = models.PositiveIntegerField()

    class Meta:
        abstract = True
    
    
class QuestionClosed(Question):
    CHOICES = (
        ('a', 'a'),
        ('b', 'b'),
        ('c', 'c'),
        ('d', 'd'),
    )
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, blank=True)
    answers_a = models.TextField()
    answers_b = models.TextField()
    answers_c = models.TextField(blank=True)
    answers_d = models.TextField(blank=True)
    correct_answer = models.CharField(max_length=1, choices=CHOICES)
    points = models.IntegerField(default=1,
                                validators=[MaxValueValidator(100), MinValueValidator(1)])
    def get_class_name(self):
        return 'questionclosed'

class ShortAnswer(Question):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answer = models.CharField(max_length=20, blank=True)
    correct_answer = models.CharField(max_length=20)
    points = models.IntegerField(default=1,
                                validators=[MaxValueValidator(100), MinValueValidator(1)])

    def get_class_name(self):
        return 'shortanswer'

class Grade(models.Model):
    test = models.ForeignKey(Test, related_name='grades', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='student_grades', on_delete=models.CASCADE)
    grade = models.IntegerField(null=True,
                                validators=[MaxValueValidator(100), MinValueValidator(1)])
    