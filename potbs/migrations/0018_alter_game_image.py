# Generated by Django 4.1 on 2023-04-09 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('potbs', '0017_event_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(blank=True, upload_to='media'),
        ),
    ]
