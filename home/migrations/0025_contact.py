# Generated by Django 3.0.6 on 2020-07-05 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_auto_20200626_0248'),
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
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
