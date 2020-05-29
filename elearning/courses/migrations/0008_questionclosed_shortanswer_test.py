# Generated by Django 3.0.4 on 2020-05-18 17:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20200518_1356'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('rating_weight', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='courses.Course')),
            ],
        ),
        migrations.CreateModel(
            name='ShortAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('answer', models.CharField(blank=True, max_length=20)),
                ('correct_answer', models.CharField(max_length=20)),
                ('points', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shortanswer_related', to='courses.Test')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuestionClosed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('answers_a', models.TextField()),
                ('answers_b', models.TextField()),
                ('answers_c', models.TextField(blank=True)),
                ('answers_d', models.TextField(blank=True)),
                ('correct_answer', models.CharField(choices=[('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')], max_length=1)),
                ('points', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionclosed_related', to='courses.Test')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
