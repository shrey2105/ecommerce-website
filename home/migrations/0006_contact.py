# Generated by Django 3.0.6 on 2020-06-21 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0005_delete_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('s_no', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=13)),
                ('mobile', models.CharField(max_length=100)),
                ('message', models.TextField()),
            ],
        ),
    ]