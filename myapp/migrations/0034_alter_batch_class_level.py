# Generated by Django 5.1 on 2024-08-24 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0033_alter_batch_class_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='class_level',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)]),
        ),
    ]
