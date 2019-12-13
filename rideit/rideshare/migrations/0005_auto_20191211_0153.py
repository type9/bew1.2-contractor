# Generated by Django 2.2.6 on 2019-12-11 01:53

from django.db import migrations
import mapbox_location_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0004_auto_20191211_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rideshare',
            name='end_location',
            field=mapbox_location_field.models.LocationField(map_attrs={}),
        ),
        migrations.AlterField(
            model_name='rideshare',
            name='start_location',
            field=mapbox_location_field.models.LocationField(map_attrs={}),
        ),
    ]