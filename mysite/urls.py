from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from articles import views

from . import settings
from .views import page_not_found, RegisterUser
urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('login/', RegisterUser.as_view(), name='login'),
    path('register/', views.login, name='register'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = page_not_found
