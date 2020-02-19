# Generated by Django 2.2.7 on 2020-02-17 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0011_community_blacklist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='blacklist',
            field=models.ManyToManyField(blank=True, help_text='The Riders that are allowed to create and participate in ridesharing in this community', related_name='BL_members_of_rideshare_community', to='rideshare.Rider'),
        ),
    ]
