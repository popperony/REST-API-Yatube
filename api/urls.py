from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from .views import PostsViewSet, GroupViewSet, CommentViewSet, FollowViewSet
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


router = DefaultRouter()
router.register('posts', PostsViewSet, basename='posts')
router.register('group', GroupViewSet, basename='group')
router.register('follow', FollowViewSet, basename='follow')
comments_router = routers.NestedSimpleRouter(router, r'posts', lookup='posts')
comments_router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(comments_router.urls)),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]
