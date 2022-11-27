from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog_post import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'likes', views.PostLikesViewSet, basename='post_likes')
router.register(r'comments', views.CommentsViewSet, basename='comments')
router.register(r'comments_likes', views.CommentsLikesViewSet, basename='comments_likes')
router.register(r'follow', views.FollowViewSet, basename='follow')


urlpatterns = [
    path('', include(router.urls)),
]