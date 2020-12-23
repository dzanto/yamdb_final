from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register('titles', views.TitleViewSet)
router.register(
    'titles/(?P<id>\d+)/reviews/(?P<review_pk>\d+)/comments',
    views.CommentViewSet, basename='perform_create_comments'
)
router.register(
    'titles/(?P<id>\d+)/reviews',
    views.ReviewViewSet, basename='perform_create_reviews'
)
router.register('categories', views.CategoryViewSet,
                basename='list_create_categories')
router.register('genres', views.GenreViewSet, basename='list_create_genres')

urlpatterns = [
    path('v1/', include(router.urls)),
]
