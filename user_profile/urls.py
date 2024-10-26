from django.urls import include, path
from .views import PasswordLessLoginView, UserProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path("password_less_login/<str:username>/", PasswordLessLoginView.as_view()),
    path('api-auth/', include('rest_framework.urls'))
]

urlpatterns += router.urls