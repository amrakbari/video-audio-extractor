import os.path

from moviepy import VideoFileClip

from layers.core.exceptions import AudioExtractionFailed
from layers.core.services import IAudioExtractorService



class AudioExtractorService(IAudioExtractorService):
    def extract(self, video_path: str, video_id: int) -> str | None:
        """
        gets a video file (str) path as input,
        extracts the audio from the video and returns the audio file's path
        in format of (str)
        """
        try:
            base_name = os.path.splitext(video_path)[0]
            audio_path = f"{base_name}.mp3"
            video_file = VideoFileClip(video_path)
            audio_file = video_file.audio
            audio_file.write_audiofile(audio_path)

            return audio_path
        except (IOError, AttributeError, ValueError) as e:
            raise AudioExtractionFailed(video_id=video_id)
