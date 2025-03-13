class AudioExtractionFailed(Exception):
    def __init__(self, video_id: int, message: str="Audio extraction failed"):
        self.video_id = video_id
        self.message = message = f"{message} for video id: {video_id}"
        super().__init__(self.message)