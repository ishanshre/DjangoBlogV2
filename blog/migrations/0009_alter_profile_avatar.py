# Generated by Django 4.1 on 2022-09-10 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_follower_profile_following_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='profile_avatar/default.png', null=True, upload_to='profile_avatar/'),
        ),
    ]
