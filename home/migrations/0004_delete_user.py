# Generated by Django 3.0.6 on 2020-06-16 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]