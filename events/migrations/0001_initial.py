# Generated by Django 5.1.4 on 2025-01-26 15:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=400)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(default='../default_post_ohnagj', upload_to='images/')),
                ('location', models.CharField(max_length=255)),
                ('event_type', models.CharField(choices=[('CONFERENCE', 'Conference'), ('MEETUP', 'Meetup'), ('WORKSHOP', 'Workshop'), ('PARTY', 'Party'), ('OTHER', 'Other')], default='OTHER', max_length=50)),
                ('event_date', models.DateTimeField(help_text='Date and time when the event will take place.')),
                ('musicians', models.ManyToManyField(blank=True, related_name='musician_events', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, help_text='Categories or tags associated with this event.', related_name='events', to='events.tag')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
