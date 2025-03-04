from abc import ABC, abstractmethod

from layers.core.entities import VideoEntity, AudioEntity


class IVideoRepository(ABC):
    @abstractmethod
    def get_video(self, video_id: int) -> VideoEntity:
        pass

    @abstractmethod
    def insert_video(self, video: VideoEntity) -> VideoEntity:
        pass


class IAudioRepository(ABC):
    @abstractmethod
    def get_audio(self, audio_id: int) -> AudioEntity:
        pass

    @abstractmethod
    def insert_audio(self, audio: AudioEntity) -> AudioEntity:
        pass