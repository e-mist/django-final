# Generated by Django 4.2.7 on 2024-05-25 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentLife_system', '0002_remove_schedule_id_schedule_sched_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='completed',
        ),
    ]