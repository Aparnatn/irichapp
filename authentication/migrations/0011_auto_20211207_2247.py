# Generated by Django 3.1.12 on 2021-12-07 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_business_details_qr_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business_details',
            name='qr_code',
        ),
        migrations.AddField(
            model_name='business_details',
            name='qrcode',
            field=models.ImageField(blank=True, null=True, upload_to='qrcode'),
        ),
    ]