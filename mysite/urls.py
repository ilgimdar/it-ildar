from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings
from .views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('articles', include('articles.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = page_not_found
