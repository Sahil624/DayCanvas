# Generated by Django 5.1.2 on 2024-10-26 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_userprofile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='interests',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='nature',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
