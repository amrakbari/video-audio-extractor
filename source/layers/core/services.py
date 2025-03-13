from abc import ABC, abstractmethod

from layers.core.entities import VideoEntity, AudioEntity


class IAudioExtractorService(ABC):
    @abstractmethod
    def extract(self, video_path: str, video_id: int) -> str:
        pass
