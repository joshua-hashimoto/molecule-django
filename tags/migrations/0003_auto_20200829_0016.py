# Generated by Django 3.1 on 2020-08-28 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_auto_20200820_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
