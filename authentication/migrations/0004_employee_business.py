# Generated by Django 3.1.12 on 2021-12-24 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20211223_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='business',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.business_details'),
        ),
    ]