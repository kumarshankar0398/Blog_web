# Generated by Django 3.2.13 on 2022-07-26 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0013_alter_preference_vote'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Preference',
            new_name='Like_Dislike',
        ),
    ]
