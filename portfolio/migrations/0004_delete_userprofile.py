# Generated by Django 5.0 on 2023-12-10 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_userprofile_email'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]