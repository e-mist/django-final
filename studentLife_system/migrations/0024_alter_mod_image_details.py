# Generated by Django 5.0.4 on 2024-06-04 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentLife_system', '0023_alter_mod_image_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mod',
            name='image_details',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
