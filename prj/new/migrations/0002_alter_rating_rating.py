# Generated by Django 4.2.2 on 2023-07-04 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(),
        ),
    ]
