# Generated by Django 5.2 on 2025-05-08 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('headsup', '0004_alter_match_players'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='location',
            field=models.CharField(default='Miami', max_length=100),
        ),
    ]
