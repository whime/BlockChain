# Generated by Django 2.1.7 on 2019-12-30 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain_project', '0002_deployedcharitycontract'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeployedFundraiseContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=100)),
                ('fundraiseName', models.CharField(max_length=100)),
                ('targetMoney', models.IntegerField()),
                ('contractAddr', models.CharField(max_length=100)),
            ],
        ),
    ]