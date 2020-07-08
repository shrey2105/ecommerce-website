# Generated by Django 3.0.6 on 2020-07-06 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_auto_20200705_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_verified',
            field=models.CharField(blank=True, choices=[('VF', 'Verified'), ('NVF', 'Not Verified')], default='NVF', max_length=4),
        ),
    ]