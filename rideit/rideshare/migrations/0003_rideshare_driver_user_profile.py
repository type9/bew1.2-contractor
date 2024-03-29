# Generated by Django 2.2.6 on 2020-03-04 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('rideshare', '0002_auto_20200304_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='rideshare',
            name='driver_user_profile',
            field=models.ForeignKey(help_text='The UserProfile of Rider who is offering to drive the trip', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='userProfile_of_rideshare_rideshare', to='accounts.UserProfile'),
        ),
    ]
