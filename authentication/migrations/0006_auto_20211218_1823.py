# Generated by Django 3.1.12 on 2021-12-18 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_employee_referral'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='role',
            new_name='designation',
        ),
    ]
