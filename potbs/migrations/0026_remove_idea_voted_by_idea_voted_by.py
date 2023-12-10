# Generated by Django 4.1 on 2023-05-15 16:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('potbs', '0025_remove_idea_vote_idea_voted_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idea',
            name='voted_by',
        ),
        migrations.AddField(
            model_name='idea',
            name='voted_by',
            field=models.ManyToManyField(blank=True, related_name='votes', to=settings.AUTH_USER_MODEL),
        ),
    ]
