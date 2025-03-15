from django.contrib import admin
from .models import Video, Audio

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'audio_extraction_status', 'created_at', 'updated_at')
    list_filter = ('audio_extraction_status',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('video', 'path', 'created_at', 'updated_at')
    search_fields = ('video__name',)
    readonly_fields = ('created_at', 'updated_at')
