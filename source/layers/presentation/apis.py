import os
import uuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.core.files.storage import default_storage
from drf_spectacular.utils import extend_schema, OpenApiResponse
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
        
    @extend_schema(
        summary='Upload Video',
        description='Upload a video file and trigger audio extraction',
        request=UploadVideoInputSerializer,
        responses={
            201: OpenApiResponse(
                response=UploadVideoOutputSerializer,
                description='Video uploaded successfully'
            ),
            400: OpenApiResponse(
                description='Invalid input'
            )
        },
        tags=['Videos']
    )
    def post(self, request):
        serializer = self.UploadVideoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        uploaded_file = validated_data["file"]
        name = validated_data["name"]
        
        file_extension = os.path.splitext(uploaded_file.name)[1]
        safe_filename = f"{uuid.uuid4()}{file_extension}"
        
        relative_path = os.path.join('videos', safe_filename)
        
        path = default_storage.save(relative_path, ContentFile(uploaded_file.read()))
        try:
        
            video = self.video_repo.insert_video(
                VideoEntity(
                    path=path,
                    name=name,
                ),
            )
        except IntegrityError as e:
            default_storage.delete(path)
            return Response(
                {"error": "Video already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        process_audio_extraction_task.delay(video.id)

        serializer = self.UploadVideoOutputSerializer(
            data={
                'path': path,
                'name': video.name,
                'audio_status': video.audio_status,
            }
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
