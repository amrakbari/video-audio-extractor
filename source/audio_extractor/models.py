from django.db import models

from common.base_model import BaseModel


class Video(BaseModel):
    path = models.FilePathField()


class Audio(BaseModel):
    path = models.FilePathField()
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)