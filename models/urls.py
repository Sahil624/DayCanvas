from django.urls import path
from .views import BatchStatus, GenerateEpisode, GenerateStory
# , StoryLineViewSet, FrameViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'stories', StoryLineViewSet, basename='story')
# router.register(r'frames', FrameViewSet, basename='frame')

urlpatterns = [
    path("story/<int:journal_id>/", GenerateStory.as_view()),
    path("episode/status/<int:batch_id>/", BatchStatus.as_view()),
    path("episode/<int:story_id>/", GenerateEpisode.as_view()),
]

# urlpatterns = router.urls
