# Generated by Django 3.1.12 on 2021-12-07 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_auto_20211207_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='business_details',
            name='qr_code',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]