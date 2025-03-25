import os.path

from django.conf import settings
from layers.core.exceptions import AudioExtractionFailed
from layers.core.services import IAudioExtractorService


class AudioExtractorService(IAudioExtractorService):
    def extract(self, video_path: str, video_id: int) -> str | None:
        """
        Gets a video file (str) path as input,
        extracts the audio from the video and returns the audio file's path
        in format of (str)
        """
        try:
            filename = os.path.basename(video_path)
            base_name = os.path.splitext(filename)[0]
            
            audio_path = f"audios/{base_name}.mp3"
            abs_audio_path = os.path.join(settings.MEDIA_ROOT, audio_path)
            abs_video_path = os.path.join(settings.MEDIA_ROOT, video_path)
            if not os.path.exists(abs_video_path):
                raise AudioExtractionFailed(video_id, 'video does not exist')
            os.makedirs(os.path.dirname(abs_audio_path), exist_ok=True)
            
            print(f"Video path: {abs_video_path}")
            print(f"Audio path: {abs_audio_path}")
            
            command = f'ffmpeg -i "{abs_video_path}" "{abs_audio_path}"'
            exit_code = os.system(command)
            
            if exit_code != 0:
                print(f"FFmpeg command failed with exit code: {exit_code}")
                raise AudioExtractionFailed(video_id=video_id)

            return audio_path
        except Exception as e:
            print(f"Error during audio extraction: {str(e)}")
            raise AudioExtractionFailed(video_id=video_id)
