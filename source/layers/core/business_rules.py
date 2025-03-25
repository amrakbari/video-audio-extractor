import os
from typing import List

from layers.core.exceptions import InvalidVideoFormatException


class VideoBusinessRules:
    ALLOWED_VIDEO_EXTENSIONS: List[str] = ['mp4', 'avi', 'mkv', 'mov']

    @classmethod
    def validate_video_format(cls, file_name: str) -> None:
        filename_parts = file_name.split('.')
        if len(filename_parts) > 1:
            extension = filename_parts[-1]
            extension = extension.lower()
        else:
            extension = ''
        
        if extension not in cls.ALLOWED_VIDEO_EXTENSIONS:
            raise InvalidVideoFormatException(extension)