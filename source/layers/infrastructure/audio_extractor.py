import os.path

from moviepy import VideoFileClip

from layers.core.services import IAudioExtractorService



class AudioExtractorService(IAudioExtractorService):
    def extract(self, video_path: str) -> str:
        """
        gets a video file (str) path as input,
        extracts the audio from the video and returns the audio file's path
        in format of (str)
        """
        base_name = os.path.splitext(video_path)[0]
        audio_path = f"{base_name}.mp3"
        video_file = VideoFileClip(video_path)
        audio_file = video_file.audio
        audio_file.write_audiofile(audio_path)

        return audio_path
