from rest_framework.routers import DefaultRouter

from story.views import JournalViewSet

router = DefaultRouter()
router.register(r'journal', JournalViewSet, basename='journal')

urlpatterns = []

urlpatterns += router.urls