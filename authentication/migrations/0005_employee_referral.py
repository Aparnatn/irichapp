# Generated by Django 3.1.12 on 2021-12-16 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_employee_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='referral',
            field=models.CharField(default=' ', max_length=150),
            preserve_default=False,
        ),
    ]