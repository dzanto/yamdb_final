from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.exceptions import ParseError
from rest_framework import viewsets, filters, generics, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.serializers import (
    CommentSerializer,
    ReviewSerializer,
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)

from api.models import Category, Genre, Title, Comment, Review, User

from api.permissions import IsOwnerOrReadOnly
from api.permissions import AdminResourcePermission, \
    SiteAdminPermission, StaffResourcePermission, ReviewCreatePermission

from api.filters import TitleFilter


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        AdminResourcePermission,
    ]
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        AdminResourcePermission,
    ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        AdminResourcePermission,
    ]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'POST']:
            return TitleWriteSerializer
        return TitleReadSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [SiteAdminPermission]

    def get_permissions(self):
        if self.request.method == 'PATCH':
            self.permission_classes = (IsOwnerOrReadOnly,)
        return super(CommentViewSet, self).get_permissions()

    def get_queryset(self):
        comment = get_object_or_404(
            Review, pk=self.kwargs['review_pk'],
            title__id=self.kwargs['id']
        )
        return comment.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   pk=self.kwargs['review_pk'],
                                   title__id=self.kwargs['id']
                                   )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [SiteAdminPermission]

    def get_permissions(self):
        if self.request.method == 'PATCH':
            self.permission_classes = (IsOwnerOrReadOnly,)
        return super(ReviewViewSet, self).get_permissions()

    def get_queryset(self):
        review = get_object_or_404(Title, id=self.kwargs['id'])
        return review.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['id'])
        serializer.save(author=self.request.user, title=title)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]
