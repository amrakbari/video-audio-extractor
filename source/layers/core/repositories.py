from abc import ABC, abstractmethod
from typing import NoReturn

from layers.core.entities import VideoEntity, AudioEntity


class IVideoRepository(ABC):
    @abstractmethod
    def get_video(self, video_id: int) -> VideoEntity:
        pass

    @abstractmethod
    def get_video_by_name(self, video_name: str) -> VideoEntity:
        pass

    @abstractmethod
    def insert_video(self, video: VideoEntity) -> VideoEntity:
        pass

    @abstractmethod
    def set_audio_status_to_error(self, video_id: int) -> None:
        pass

    @abstractmethod
    def set_audio_status_to_completed(self, video_id: int) -> None:
        pass

    @abstractmethod
    def set_audio_status_to_in_progress(self, video_id: int) -> None:
        pass

    @abstractmethod
    def get_video_and_set_audio_status_to_declared_status(self, video_id: int, status: str) -> VideoEntity:
        pass


class IAudioRepository(ABC):
    @abstractmethod
    def get_audio(self, audio_id: int) -> AudioEntity:
        pass

    @abstractmethod
    def insert_audio(self, audio: AudioEntity) -> AudioEntity:
        pass