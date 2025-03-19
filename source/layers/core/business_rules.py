import os
from typing import List

from layers.core.exceptions import InvalidVideoFormatException


class VideoBusinessRules:
    ALLOWED_VIDEO_EXTENSIONS: List[str] = ['mp4', 'avi', 'mkv', 'mov']

    @classmethod
    def validate_video_format(cls, file_name: str) -> None:
        _, extension = file_name.split('.')
        extension = extension.lower()
        
        if extension not in cls.ALLOWED_VIDEO_EXTENSIONS:
            raise InvalidVideoFormatException(extension)