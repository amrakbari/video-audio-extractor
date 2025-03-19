import pytest
from layers.core.business_rules import VideoBusinessRules
from layers.core.exceptions import InvalidVideoFormatException


class TestVideoBusinessRules:
    def test_validate_video_format_valid(self):
        """Test that valid video formats are accepted"""
        valid_formats = [
            "video.mp4",
            "movie.avi",
            "clip.mkv",
            "film.mov"
        ]
        
        for filename in valid_formats:
            # Should not raise any exception
            VideoBusinessRules.validate_video_format(filename)

    def test_validate_video_format_invalid(self):
        """Test that invalid video formats raise InvalidVideoFormatException"""
        invalid_formats = [
            "video.xyz",
            "movie.txt",
            "clip.pdf",
            "film.doc"
        ]
        
        for filename in invalid_formats:
            with pytest.raises(InvalidVideoFormatException):
                VideoBusinessRules.validate_video_format(filename)

    def test_validate_video_format_no_extension(self):
        """Test that files without extensions are rejected"""
        with pytest.raises(InvalidVideoFormatException):
            VideoBusinessRules.validate_video_format("video")

    def test_validate_video_format_empty_filename(self):
        """Test that empty filenames are rejected"""
        with pytest.raises(InvalidVideoFormatException):
            VideoBusinessRules.validate_video_format("") 