# Generated by Django 3.0.4 on 2020-05-04 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20200430_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='learning_style',
            field=models.CharField(choices=[('wzrokowiec', 'wzrokowiec'), ('słuchowiec', 'słuchowiec'), ('dotykowiec', 'dotykowiec'), ('kinestetyk', 'kinestetyk')], default=0, max_length=10),
            preserve_default=False,
        ),
    ]
