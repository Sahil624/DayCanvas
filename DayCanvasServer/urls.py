"""
URL configuration for DayCanvasServer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views import static

from DayCanvasServer import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('user_profile.urls')),
    path('story/', include('story.urls')),
    path('models/', include('models.urls')),
    # path(r'^images/(?P<path>.*)$', static.serve, {'document_root': settings.BASE_DIR.joinpath("/images")}),
    path('images/<path:path>', static.serve, {
        'document_root': settings.BASE_DIR.joinpath('images')
    }),
]
