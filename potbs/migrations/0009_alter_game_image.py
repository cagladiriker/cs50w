# Generated by Django 4.1 on 2023-01-08 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('potbs', '0008_alter_team_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
