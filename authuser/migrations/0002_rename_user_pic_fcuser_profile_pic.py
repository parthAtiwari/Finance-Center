# Generated by Django 4.1.7 on 2023-04-09 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fcuser',
            old_name='user_pic',
            new_name='profile_pic',
        ),
    ]
