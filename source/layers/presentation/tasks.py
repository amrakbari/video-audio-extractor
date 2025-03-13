from celery import shared_task

from layers.application.use_cases import AudioExtractionUseCase
from layers.core.exceptions import AudioExtractionFailed
from layers.infrastructure.audio_extractor import AudioExtractorService
from layers.infrastructure.repositories import VideoRepository, AudioRepository


@shared_task(
    autoretry_for=(AudioExtractionFailed,),
    retry_backoff=30,
    retry_backoff_max=300,
    max_retries=3
)
def process_audio_extraction_task(video_id: int):
    try:
        use_case = AudioExtractionUseCase(
            video_repo=VideoRepository(),
            audio_repo=AudioRepository(),
            audio_extractor_service=AudioExtractorService()
        )
        use_case.execute(video_id)
    except AudioExtractionFailed as e:
        VideoRepository().set_audio_status_to_error(video_id=video_id)