# Generated by Django 3.2.5 on 2021-07-15 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210715_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
    ]
