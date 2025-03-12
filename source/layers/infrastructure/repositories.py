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
        video = get_object_or_404(Video, id=video_id)
        return VideoEntity(
            id=video.id,
            name=video.name,
            path=video.path,
        )

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
