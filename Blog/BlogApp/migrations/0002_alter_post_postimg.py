# Generated by Django 3.2.13 on 2022-07-19 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postImg',
            field=models.ImageField(blank=True, null=True, upload_to='postimg'),
        ),
    ]