import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from layers.core.entities import VideoEntity
from layers.infrastructure.repositories import VideoRepository, AudioRepository
from layers.presentation.tasks import process_audio_extraction_task


class VideoAPIView(APIView):
    def __init__(self):
        super().__init__()
        self.video_repo = VideoRepository()
        self.audio_repo = AudioRepository()

    class UploadVideoInputSerializer(serializers.Serializer):
        file = serializers.FileField()
        name = serializers.CharField(max_length=255)

    class UploadVideoOutputSerializer(serializers.Serializer):
        path = serializers.CharField(max_length=2000)
        name = serializers.CharField(max_length=255)
        audio_status = serializers.CharField(max_length=20)

    def post(self, request):
        serializer = self.UploadVideoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        file = validated_data["file"]
        name = validated_data["name"]
        file_path = os.path.join(settings.MEDIA_ROOT, 'videos', str(file))
        path = default_storage.save(file_path, ContentFile(file.read()))
        video = self.video_repo.insert_video(
            VideoEntity(
                path=path,
                name=name,
            ),
        )

        process_audio_extraction_task.delay(video.id)

        serializer = self.UploadVideoOutputSerializer(
            path=video.path,
            name=video.name,
            audio_status=video.audio_status,
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



