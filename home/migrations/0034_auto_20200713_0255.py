# Generated by Django 3.0.6 on 2020-07-13 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_forgotpasswordotp_is_validated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forgotpasswordotp',
            name='is_validated',
            field=models.CharField(blank=True, choices=[('VF', 'Verified'), ('NF', 'Not Verified')], default='NF', max_length=2),
        ),
    ]
