from django.contrib import admin
from django.utils.html import format_html

from models.models import Frame, FrameImages, ImageGenBatch, StoryLine

class FrameInline(admin.TabularInline):
    model = Frame
    extra = 1
    readonly_fields = ['story', 'image_gen_prompt', 'image_preview']


    def image_preview(self, obj):
        if obj.frameimages.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 250px;"/>',
                obj.frameimages.image.url
            )
        return 'No image'
    image_preview.short_description = 'Image Preview'


@admin.register(StoryLine)
class StoryLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'get_frame_count', 'created_date']
    list_filter = ['user']
    search_fields = ['title', 'summary', 'user__username']
    readonly_fields = ['response']
    inlines = [FrameInline]
    
    def get_frame_count(self, obj):
        return obj.frame_set.count()
    get_frame_count.short_description = 'Frames'
    
    def created_date(self, obj):
        return obj.journal.created_on
    created_date.short_description = 'Created On'


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_story_title', 'get_user']
    list_filter = ['storyline__user']
    search_fields = ['storyline__title', 'story', 'storyline__user__username']
    
    def get_story_title(self, obj):
        return obj.storyline.title
    get_story_title.short_description = 'Story'
    
    def get_user(self, obj):
        return obj.storyline.user
    get_user.short_description = 'User'



@admin.register(ImageGenBatch)
class ImageGenBatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'storyline', 'completed_count', 'completion_status', 
                   'started_at', 'updated_at', 'time_elapsed')
    list_filter = ('started_at', 'updated_at')
    search_fields = ('storyline__title', 'id')
    readonly_fields = ('started_at', 'updated_at')
    
  
    def completion_status(self, obj):
        total_frames = obj.storyline.frame_set.count()
        return 'Completed' if obj.completed_count == total_frames else 'Not Completed'
    completion_status.short_description = 'Status'

    def time_elapsed(self, obj):
        if obj.updated_at and obj.started_at:
            elapsed = obj.updated_at - obj.started_at
            hours = elapsed.seconds // 3600
            minutes = (elapsed.seconds % 3600) // 60
            return '{0}h {1}m'.format(hours, minutes)
        return '-'
    time_elapsed.short_description = 'Time Elapsed'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('storyline')


@admin.register(FrameImages)
class FrameImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'frame', 'batch', 'image_preview', 'created_at')
    list_filter = ('created_at', 'batch')
    search_fields = ('frame__title', 'batch__id')
    readonly_fields = ('created_at', 'image_preview')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;"/>',
                obj.image.url
            )
        return 'No image'
    image_preview.short_description = 'Image Preview'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('frame', 'batch')