from django.urls import path

from layers.presentation.apis import VideoAPIView, AudioExtractionStatusApiView, AudioApiView

urlpatterns = [
    path('videos/', VideoAPIView.as_view(), name='video-upload'),
    path('videos/result/<str:video_name>/', AudioExtractionStatusApiView.as_view(), name='audio-extraction-status'),
    path('audios/<str:video_name>/', AudioApiView.as_view(), name='audio-api'),
] 