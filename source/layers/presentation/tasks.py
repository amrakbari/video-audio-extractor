from celery import shared_task
from celery.exceptions import MaxRetriesExceededError

from layers.application.use_cases import AudioExtractionUseCase
from layers.core.exceptions import AudioExtractionFailed
from layers.infrastructure.audio_extractor import AudioExtractorService
from layers.infrastructure.repositories import VideoRepository, AudioRepository


@shared_task(
    autoretry_for=(AudioExtractionFailed,),
    default_retry_delay=30,
    max_retries=3,
    acks_late=True
)
def process_audio_extraction_task(video_id: int):
    try:
        use_case = AudioExtractionUseCase(
            video_repo=VideoRepository(),
            audio_repo=AudioRepository(),
            audio_extractor_service=AudioExtractorService()
        )
        use_case.execute(video_id)
        print('audio extraction task completed successfully')
    except AudioExtractionFailed as e:
        print('error:', e.message)
        current_retries = process_audio_extraction_task.request.retries
        max_retries = process_audio_extraction_task.max_retries
        
        if current_retries >= max_retries:
            VideoRepository().set_audio_status_to_error(video_id=video_id)
        raise e