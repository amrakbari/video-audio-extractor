from layers.core.entities import VideoEntity
from layers.core.repositories import IAudioRepository, IVideoRepository
from layers.core.services import IAudioExtractorService


class CreateVideoUseCase:
    def __init__(self, repository: IVideoRepository):
        self.repository = repository

    def execute(self, path: str, size: float):
        video = VideoEntity(path=path, size=size)
        video = self.repository.insert_video(video)
        return video

class ExtractAudioUseCase:
    def __init__(self, video_repository: IVideoRepository, audio_repository: IAudioRepository, video_extractor_service: IAudioExtractorService):
        self.video_repository = video_repository
        self.audio_repository = audio_repository
        self.video_extractor_service = video_extractor_service

    def execute(self, video_id: int):
        obj = self.video_repository.get_video(video_id)
        video = VideoEntity(path=obj.path, size=obj.size)
        audio = self.video_extractor_service.extract_audio(video)
        self.audio_repository.insert_audio(audio)



