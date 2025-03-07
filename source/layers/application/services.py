from layers.core.entities import AudioEntity
from layers.core.repositories import IVideoRepository, IAudioRepository
from layers.core.services import IAudioExtractorService


class AudioExtractionService:
    def __init__(self, video_repo: IVideoRepository, audio_repo: IAudioRepository, audio_extractor_service: IAudioExtractorService):
        self.video_repo = video_repo
        self.audio_repo = audio_repo
        self.audio_extractor_service = audio_extractor_service

    def extract_audio(self, video_id: int) -> AudioEntity:
        video = self.video_repo.get_video(video_id)
        audio_path = self.audio_extractor_service.extract(video.path)
        audio = AudioEntity(
            video_id=video_id,
            path=audio_path,
        )
        audio = self.audio_repo.insert_audio(audio)
        return audio
