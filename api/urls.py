from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from .views import PostsViewSet, CommentViewSet, GroupViewSet
from rest_framework_nested import routers


router = DefaultRouter()
router.register('posts', PostsViewSet, basename='posts')
comments_router = routers.NestedSimpleRouter(router, r'posts', lookup='posts')
comments_router.register(r'comments', CommentViewSet, basename='comments')
group_router = routers.SimpleRouter()
group_router.register('group', GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls)),
    path('', include(group_router.urls))
]