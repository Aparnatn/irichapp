# Generated by Django 3.1.12 on 2021-12-14 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_business_details_in'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business_details',
            name='add_offer',
        ),
    ]