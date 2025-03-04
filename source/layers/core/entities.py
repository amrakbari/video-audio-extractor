from dataclasses import dataclass


@dataclass
class VideoEntity:
    path: str
    size: float

    def __init__(self, path: str, size: float):
        self.path = path
        self.size = size

@dataclass
class AudioEntity:
    video_id: int
    path: str
    size: float
    def __init__(self, video_id: int, path: str):
        self.video_id = video_id
        self.path = path