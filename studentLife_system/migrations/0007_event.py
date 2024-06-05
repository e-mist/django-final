# Generated by Django 5.0.3 on 2024-06-01 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentLife_system', '0006_graduateform'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('eventID', models.AutoField(primary_key=True, serialize=False)),
                ('eventsName', models.CharField(max_length=100)),
                ('eventsDate', models.DateField()),
                ('eventsLocation', models.CharField(max_length=100)),
                ('eventsDescription', models.TextField()),
                ('eventsImage', models.ImageField(blank=True, null=True, upload_to='event_images/')),
            ],
        ),
    ]