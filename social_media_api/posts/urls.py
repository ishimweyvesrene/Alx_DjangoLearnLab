from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, PostLikeToggleAPIView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:pk>/like/', PostLikeToggleAPIView.as_view(), name='post-like'),
     path('<int:pk>/unlike/', views.unlike_post, name='unlike-post'),
]

