# Generated by Django 2.1.7 on 2020-01-04 23:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain_project', '0004_auto_20200103_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployrequest',
            name='state',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)]),
        ),
    ]
