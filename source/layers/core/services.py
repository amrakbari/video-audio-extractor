from abc import ABC

from layers.core.entities import VideoEntity, AudioEntity


class IAudioExtractorService(ABC):
    @classmethod
    def extract(cls, video_path: str) -> str:
        pass
