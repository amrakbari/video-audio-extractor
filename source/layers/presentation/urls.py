from django.urls import path

from layers.presentation.apis import VideoAPIView

urlpatterns = [
    path('videos/', VideoAPIView.as_view(), name='video-upload'),
] 