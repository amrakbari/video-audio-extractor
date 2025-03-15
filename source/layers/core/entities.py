from dataclasses import dataclass


@dataclass
class VideoEntity:
    path: str
    name: str
    id: int | None = None
    audio_status: str | None = None

@dataclass
class AudioEntity:
    video_id: int
    path: str
    id: int | None = None
