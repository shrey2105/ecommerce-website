# Generated by Django 3.1 on 2020-08-23 03:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('heading1', models.CharField(default='', max_length=500)),
                ('content_heading1', models.TextField()),
                ('heading2', models.CharField(default='', max_length=500)),
                ('content_heading2', models.TextField()),
                ('sub_heading', models.CharField(default='', max_length=500)),
                ('sub_heading_content', models.TextField()),
                ('pub_date', models.DateField(blank=True, null=True)),
                ('author', models.CharField(default='', max_length=30)),
                ('thumbnail', models.ImageField(blank=True, default='', null=True, upload_to='blog/images')),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Unpublished', 'Unpublished'), ('Featured', 'Featured')], default='Unpublished', max_length=120)),
            ],
        ),
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
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField(default='')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.blogcomment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blogpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
