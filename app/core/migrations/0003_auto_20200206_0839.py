# Generated by Django 2.1.15 on 2020-02-06 08:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200206_0626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nome',
            field=models.CharField(blank=True, max_length=255, validators=[django.core.validators.RegexValidator('A-Za-z', message='Password should be a combination of Alphabets and Numbers')], verbose_name='Nome'),
        ),
    ]