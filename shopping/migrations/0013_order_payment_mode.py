# Generated by Django 3.1 on 2020-09-05 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0012_auto_20200905_0615'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_mode',
            field=models.CharField(blank=True, default='0', max_length=100, null=True),
        ),
    ]