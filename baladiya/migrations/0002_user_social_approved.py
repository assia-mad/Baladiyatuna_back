# Generated by Django 4.2.2 on 2023-07-01 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baladiya', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='social_approved',
            field=models.BooleanField(default=False),
        ),
    ]
