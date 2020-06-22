# Generated by Django 3.0.6 on 2020-06-16 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=13)),
                ('message', models.TextField()),
            ],
        ),
    ]