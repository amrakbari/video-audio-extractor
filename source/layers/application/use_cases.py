from layers.core.entities import AudioEntity
from layers.core.repositories import IVideoRepository, IAudioRepository
from layers.core.services import IAudioExtractorService


class AudioExtractionUseCase:
    def __init__(self, video_repo: IVideoRepository, audio_repo: IAudioRepository, audio_extractor_service: IAudioExtractorService):
        self.video_repo = video_repo
        self.audio_repo = audio_repo
        self.audio_extractor_service = audio_extractor_service

    def execute(self, video_id: int) -> AudioEntity:
        video = self.video_repo.get_video_and_set_audio_status_to_declared_status(video_id, 'progress')
        audio_path = self.audio_extractor_service.extract(video.path, video.id)
        self.video_repo.set_audio_status_to_completed(video.id)
        audio = AudioEntity(
            video_id=video.id,
            path=audio_path,
        )
        audio = self.audio_repo.insert_audio(audio)
        return audio
