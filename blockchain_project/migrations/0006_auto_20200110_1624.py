# Generated by Django 2.1.7 on 2020-01-10 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain_project', '0005_auto_20200104_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployedcharitycontract',
            name='owner',
            field=models.CharField(max_length=50),
        ),
    ]