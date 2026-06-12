from django.contrib import admin
from django.urls import path, include
from frontend import views as frontend_views
from django.conf import settings  # ← ADD THIS IMPORT
from django.conf.urls.static import static 

urlpatterns = [
    path('', frontend_views.index, name='index'),
    path('chat/', frontend_views.chat, name='chat'),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)