# Generated by Django 3.2.1 on 2021-09-04 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210626_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='tcamera',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]