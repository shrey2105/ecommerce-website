# Generated by Django 3.1 on 2020-08-22 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0005_bannerimage_fourth_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='post_office',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
