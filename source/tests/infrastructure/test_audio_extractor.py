import os
import pytest
from unittest.mock import patch, Mock
from django.conf import settings
from layers.infrastructure.audio_extractor import AudioExtractorService
from layers.core.exceptions import AudioExtractionFailed


class TestAudioExtractorService:
    @pytest.fixture
    def service(self):
        return AudioExtractorService()

    @pytest.fixture
    def mock_video_path(self):
        return "videos/test.mp4"

    @pytest.fixture
    def mock_audio_path(self):
        return "audios/test.mp3"

    def test_extract_success(self, service, mock_video_path, mock_audio_path):
        """Test successful audio extraction"""
        video_id = 1
        abs_video_path = os.path.join(settings.MEDIA_ROOT, mock_video_path)
        abs_audio_path = os.path.join(settings.MEDIA_ROOT, mock_audio_path)
        
        with patch('os.path.exists') as mock_exists, \
             patch('os.system') as mock_system, \
             patch('os.makedirs') as mock_makedirs:
            mock_exists.return_value = True
            mock_system.return_value = 0
            
            result = service.extract(mock_video_path, video_id)
            
            assert result == mock_audio_path
            expected_command = f'ffmpeg -i "{abs_video_path}" "{abs_audio_path}"'
            mock_system.assert_called_with(expected_command)
            mock_makedirs.assert_called_once()

    def test_extract_video_not_found(self, service, mock_video_path):
        """Test when video file doesn't exist"""
        video_id = 1
        
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            
            with pytest.raises(AudioExtractionFailed) as exc_info:
                service.extract(mock_video_path, video_id)

    def test_extract_ffmpeg_failed(self, service, mock_video_path):
        """Test when ffmpeg command fails"""
        video_id = 1
        
        with patch('os.path.exists') as mock_exists, \
             patch('os.system') as mock_system, \
             patch('os.makedirs'):
            mock_exists.return_value = True
            mock_system.return_value = 1  # Non-zero exit code indicates failure
            
            with pytest.raises(AudioExtractionFailed) as exc_info:
                service.extract(mock_video_path, video_id)

    def test_extract_unexpected_error(self, service, mock_video_path):
        """Test when an unexpected error occurs"""
        # Arrange
        video_id = 1
        
        # Mock file existence and force an exception
        with patch('os.path.exists') as mock_exists:
            mock_exists.side_effect = Exception("Unexpected error")
            
            # Act & Assert
            with pytest.raises(AudioExtractionFailed) as exc_info:
                service.extract(mock_video_path, video_id)