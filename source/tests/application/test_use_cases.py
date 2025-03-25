import pytest
from unittest.mock import Mock, patch
from layers.core.entities import VideoEntity, AudioEntity
from layers.application.use_cases import AudioExtractionUseCase
from layers.core.exceptions import AudioExtractionFailed, InvalidVideoFormatException
from layers.core.business_rules import VideoBusinessRules


class TestAudioExtractionUseCase:
    @pytest.fixture
    def mock_video_repo(self):
        return Mock()

    @pytest.fixture
    def mock_audio_repo(self):
        return Mock()

    @pytest.fixture
    def mock_audio_extractor(self):
        return Mock()

    @pytest.fixture
    def use_case(self, mock_video_repo, mock_audio_repo, mock_audio_extractor):
        return AudioExtractionUseCase(
            video_repo=mock_video_repo,
            audio_repo=mock_audio_repo,
            audio_extractor_service=mock_audio_extractor
        )

    def test_execute_success(self, use_case, mock_video_repo, mock_audio_repo, mock_audio_extractor):
        """Test successful audio extraction"""
        video_id = 1
        video_path = "videos/test.mp4"
        audio_path = "audios/test.mp3"
        
        mock_video = VideoEntity(
            id=video_id,
            path=video_path,
            name="test.mp4",
            audio_status="progress"
        )
        mock_audio = AudioEntity(
            video_id=video_id,
            path=audio_path
        )
        
        mock_video_repo.get_video_and_set_audio_status_to_declared_status.return_value = mock_video
        mock_audio_extractor.extract.return_value = audio_path
        
        use_case.execute(video_id)
        
        mock_video_repo.get_video_and_set_audio_status_to_declared_status.assert_called_once_with(video_id, 'progress')
        mock_audio_extractor.extract.assert_called_once_with(video_path, video_id)
        mock_video_repo.set_audio_status_to_completed.assert_called_once_with(video_id)
        mock_audio_repo.insert_audio.assert_called_once_with(mock_audio)
        mock_video_repo.set_audio_status_to_completed.assert_called_once_with(video_id)

    def test_execute_video_not_found(self, use_case, mock_video_repo):
        """Test when video is not found"""
        video_id = 1
        mock_video_repo.get_video_and_set_audio_status_to_declared_status.return_value = None
        
        with pytest.raises(AudioExtractionFailed) as exc_info:
            use_case.execute(video_id)
        assert "Video not found" in str(exc_info.value)

    def test_execute_extraction_failed(self, use_case, mock_video_repo, mock_audio_extractor):
        """Test when audio extraction fails"""
        # Arrange
        video_id = 1
        video_path = "videos/test.mp4"
        
        mock_video = VideoEntity(
            id=video_id,
            path=video_path,
            name="test.mp4",
            audio_status="progress"
        )
        
        mock_video_repo.get_video_and_set_audio_status_to_declared_status.return_value = mock_video
        mock_audio_extractor.extract.side_effect = AudioExtractionFailed(video_id=video_id)
        
        with pytest.raises(AudioExtractionFailed):
            use_case.execute(video_id)
        

    def test_execute_invalid_video_format(self, use_case, mock_video_repo):
        """Test when video format is invalid"""
        video_id = 1
        video_path = "videos/test.xyz"
        
        mock_video = VideoEntity(
            id=video_id,
            path=video_path,
            name="test.xyz",
            audio_status="progress"
        )
        
        mock_video_repo.get_video_and_set_audio_status_to_declared_status.return_value = mock_video
        
        with pytest.raises(InvalidVideoFormatException):
            use_case.execute(video_id) 