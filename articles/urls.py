from django.urls import path
from . import views
from .views import PostList, PostCat

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('new/', views.post_new, name='post_new'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/delete/ok/', views.post_delete, name='post_delete'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('category/<int:cat_id>/', PostCat.as_view(), name='category')
]
