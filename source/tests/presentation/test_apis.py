import pytest

from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.db import IntegrityError
from rest_framework import status
from layers.presentation.apis import VideoAPIView
from layers.core.exceptions import InvalidVideoFormatException


class TestVideoAPIView:
    @pytest.fixture
    def api_view(self):
        return VideoAPIView()

    @pytest.fixture
    def factory(self):
        return RequestFactory()

    @pytest.fixture
    def valid_video_file(self):
        return SimpleUploadedFile(
            "test.mp4",
            b"file_content",
            content_type="video/mp4"
        )

    @pytest.fixture
    def invalid_video_file(self):
        return SimpleUploadedFile(
            "test.xyz",
            b"file_content",
            content_type="application/octet-stream"
        )

    def test_post_success(self, api_view, factory, valid_video_file):
        """Test successful video upload"""
        request = factory.post(
            '/api/videos/',
            {
                'file': valid_video_file,
                'name': 'Test Video'
            },
            format='multipart'
        )

        response = api_view.post(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert 'path' in response.data
        assert 'name' in response.data
        assert response.data['audio_status'] == 'pending'
        assert response.data['name'] == 'Test Video'

    def test_post_invalid_format(self, api_view, factory, invalid_video_file):
        """Test upload with invalid video format"""
        request = factory.post(
            '/api/videos/',
            {
                'file': invalid_video_file,
                'name': 'Test Video'
            },
            format='multipart'
        )

        response = api_view.post(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert 'Invalid video format' in response.data['error']

    def test_post_missing_file(self, api_view, factory):
        """Test upload without file"""
        request = factory.post(
            '/api/videos/',
            {
                'name': 'Test Video'
            },
            format='multipart'
        )

        response = api_view.post(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'file' in response.data

    def test_post_missing_name(self, api_view, factory, valid_video_file):
        """Test upload without name"""
        request = factory.post(
            '/api/videos/',
            {
                'file': valid_video_file
            },
            format='multipart'
        )

        response = api_view.post(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data

    def test_post_duplicate_video(self, api_view, factory, valid_video_file):
        """Test upload of duplicate video"""
        request = factory.post(
            '/api/videos/',
            {
                'file': valid_video_file,
                'name': 'Test Video'
            },
            format='multipart'
        )

        with patch('layers.infrastructure.repositories.VideoRepository.insert_video') as mock_insert:
            mock_insert.side_effect = IntegrityError()

            response = api_view.post(request)

            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert 'error' in response.data
            assert 'Video already exists' in response.data['error']