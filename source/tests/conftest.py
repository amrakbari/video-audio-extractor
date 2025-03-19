import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from layers.core.entities import VideoEntity, AudioEntity


@pytest.fixture
def sample_video_entity():
    """Fixture for a sample video entity"""
    return VideoEntity(
        id=1,
        path="videos/test.mp4",
        name="test.mp4",
        audio_status="pending"
    )


@pytest.fixture
def sample_audio_entity():
    """Fixture for a sample audio entity"""
    return AudioEntity(
        id=1,
        path="audios/test.mp3",
        video_id=1
    )


@pytest.fixture
def valid_video_file():
    """Fixture for a valid video file"""
    return SimpleUploadedFile(
        "test.mp4",
        b"file_content",
        content_type="video/mp4"
    )


@pytest.fixture
def invalid_video_file():
    """Fixture for an invalid video file"""
    return SimpleUploadedFile(
        "test.xyz",
        b"file_content",
        content_type="application/octet-stream"
    ) 