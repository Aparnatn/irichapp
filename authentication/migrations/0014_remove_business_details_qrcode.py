# Generated by Django 3.1.12 on 2021-12-08 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_business_details_qrcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business_details',
            name='qrcode',
        ),
    ]