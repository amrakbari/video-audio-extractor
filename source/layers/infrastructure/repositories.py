from typing import NoReturn

from django.db import models
from rest_framework.generics import get_object_or_404

from audio_extractor.models import Video, Audio
from layers.core.entities import AudioEntity, VideoEntity
from layers.core.repositories import IVideoRepository, IAudioRepository


class VideoRepository(IVideoRepository):
    def __init__(self):
        self.model = Video

    def insert_video(self, video: VideoEntity) -> VideoEntity:
        video_object = self.model.objects.create(
            path=video.path,
            name=video.name,
        )
        return VideoEntity(
            id=video_object.id,
            name=video.name,
            path=video_object.path,
            audio_status=video_object.audio_extraction_status,
        )

    def get_video(self, video_id: int) -> VideoEntity:
        video = get_object_or_404(self.model, id=video_id)
        return VideoEntity(
            id=video.id,
            name=video.name,
            path=video.path,
            audio_status=video.audio_extraction_status,
        )

    def get_video_and_set_audio_status_to_declared_status(self, video_id: int, status: str) -> VideoEntity:
        video = get_object_or_404(self.model, id=video_id)
        video.audio_extraction_status = status
        video.save()
        return VideoEntity(
            id=video.id,
            name=video.name,
            path=video.path,
            audio_status=video.audio_extraction_status,
        )

    def set_audio_status_to_in_progress(self, video_id: int) -> None:
        self.model.objects.filter(id=video_id).update(audio_extraction_status='progress')

    def set_audio_status_to_completed(self, video_id: int) -> None:
        self.model.objects.filter(id=video_id).update(audio_extraction_status='completed')

    def set_audio_status_to_error(self, video_id: int) -> None:
        self.model.objects.filter(id=video_id).update(audio_extraction_status='error')


class AudioRepository(IAudioRepository):
    def __init__(self):
        self.model = Audio

    def insert_audio(self, audio: AudioEntity) -> AudioEntity:
        audio = self.model.objects.create(
            path=audio.path,
            video_id=audio.video_id,
        )
        return AudioEntity(
            id=audio.id,
            path=audio.path,
            video_id=audio.video_id,
        )

    def get_audio(self, audio_id: int) -> AudioEntity:
        audio = get_object_or_404(Audio, id=audio_id)
        return AudioEntity(
            id=audio.id,
            path=audio.path,
            video_id=audio.videoـid,
        )
