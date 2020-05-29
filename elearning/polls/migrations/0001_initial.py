# Generated by Django 3.0.4 on 2020-04-29 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=500)),
                ('choice_1', models.CharField(max_length=500)),
                ('choice_2', models.CharField(max_length=500)),
                ('choice_3', models.CharField(max_length=500)),
                ('choice_4', models.CharField(max_length=500)),
            ],
        ),
    ]
