from layers.core.entities import AudioEntity
from layers.core.repositories import IVideoRepository, IAudioRepository
from layers.core.services import IAudioExtractorService
from layers.core.exceptions import AudioExtractionFailed
from layers.core.business_rules import VideoBusinessRules


class AudioExtractionUseCase:
    def __init__(self, video_repo: IVideoRepository, audio_repo: IAudioRepository, audio_extractor_service: IAudioExtractorService):
        self.video_repo = video_repo
        self.audio_repo = audio_repo
        self.audio_extractor_service = audio_extractor_service

    def execute(self, video_id: int) -> AudioEntity:
        video = self.video_repo.get_video_and_set_audio_status_to_declared_status(video_id, 'progress')
        if not video:
            raise AudioExtractionFailed(video_id, f"Video not found for id: {video_id}")
        VideoBusinessRules.validate_video_format(video.path)
        audio_path = self.audio_extractor_service.extract(video.path, video.id)
        self.video_repo.set_audio_status_to_completed(video.id)
        audio = AudioEntity(
            video_id=video.id,
            path=audio_path,
        )
        audio = self.audio_repo.insert_audio(audio)
        return audio
