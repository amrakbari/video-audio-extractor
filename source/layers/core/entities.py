from dataclasses import dataclass


@dataclass
class VideoEntity:
    id: int
    path: str

@dataclass
class AudioEntity:
    video_id: int
    path: str
    id: int | None = None
