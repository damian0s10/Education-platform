# Generated by Django 3.0.4 on 2020-03-23 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_choice_4'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='choice_1',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='question',
            name='choice_2',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='question',
            name='choice_3',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='question',
            name='choice_4',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=250),
        ),
    ]
