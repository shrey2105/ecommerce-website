# Generated by Django 3.0.6 on 2020-07-23 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0014_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='subject',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
