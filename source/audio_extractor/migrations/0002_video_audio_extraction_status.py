# Generated by Django 5.1.6 on 2025-03-12 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio_extractor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='audio_extraction_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('progress', 'In Progress'), ('completed', 'Completed'), ('error', 'Error')], default='pending', max_length=20),
        ),
    ]
