# Generated by Django 3.0.4 on 2020-05-29 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20200529_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionclosed',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionclosed', to='courses.Test'),
        ),
        migrations.AlterField(
            model_name='shortanswer',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shortanswer', to='courses.Test'),
        ),
    ]
