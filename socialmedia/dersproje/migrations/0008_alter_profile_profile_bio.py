# Generated by Django 4.2.6 on 2023-12-28 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dersproje', '0007_profile_facebook_link_profile_homepage_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]