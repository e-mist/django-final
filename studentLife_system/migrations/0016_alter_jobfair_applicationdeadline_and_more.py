# Generated by Django 4.2.11 on 2024-06-03 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentLife_system', '0015_merge_20240604_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobfair',
            name='applicationdeadline',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='jobfair',
            name='posted_date',
            field=models.DateField(),
        ),
    ]
