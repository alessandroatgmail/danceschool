# Generated by Django 2.1.15 on 2020-02-06 06:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nome',
            field=models.CharField(blank=True, max_length=255, validators=[django.core.validators.RegexValidator('[A-Za-z]', message='Password should be a combination of Alphabets and Numbers')], verbose_name='Nome'),
        ),
    ]
