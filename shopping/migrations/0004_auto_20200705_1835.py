# Generated by Django 3.0.6 on 2020-07-05 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0003_auto_20200705_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerimage',
            name='first_image_url',
            field=models.ImageField(blank=True, null=True, upload_to='shopping/images'),
        ),
        migrations.AlterField(
            model_name='bannerimage',
            name='second_image_url',
            field=models.ImageField(blank=True, null=True, upload_to='shopping/images'),
        ),
        migrations.AlterField(
            model_name='bannerimage',
            name='third_image_url',
            field=models.ImageField(blank=True, null=True, upload_to='shopping/images'),
        ),
    ]