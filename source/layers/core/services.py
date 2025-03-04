from abc import ABC

from layers.core.entities import VideoEntity, AudioEntity


class IAudioExtractorService(ABC):
    @classmethod
    def extract_audio(cls, video: VideoEntity) -> AudioEntity:
        pass
