from django.db import models

from common.base_model import BaseModel


class Video(BaseModel):
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'progress'
    STATUS_COMPLETED = 'completed'
    STATUS_ERROR = 'error'
    AUDIO_EXTRACTION_STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_ERROR, 'Error'),
    )

    path = models.FileField(upload_to='videos/', max_length=1000)
    name = models.CharField(max_length=255, unique=True)
    audio_extraction_status = models.CharField(max_length=20, choices=AUDIO_EXTRACTION_STATUS_CHOICES, default=STATUS_PENDING)


class Audio(BaseModel):
    path = models.FileField(upload_to='audios/', max_length=1000)
    video = models.OneToOneField(Video, on_delete=models.SET_NULL, null=True)