# Generated by Django 5.0.6 on 2024-06-03 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentLife_system', '0012_intakeinverview_intakeid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuidanceTransaction',
            fields=[
                ('transactionId', models.AutoField(primary_key=True, serialize=False)),
                ('transactionType', models.CharField(max_length=255)),
                ('transactionDate', models.DateField(max_length=255)),
            ],
        ),
    ]