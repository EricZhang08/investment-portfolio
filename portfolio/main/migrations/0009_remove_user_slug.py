# Generated by Django 3.2.5 on 2021-07-16 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_user_portfolio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='slug',
        ),
    ]
