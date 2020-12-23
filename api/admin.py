from django.contrib import admin
from api.models import Category, Genre, Title, Comment, Review
from django.apps import apps


class CommentAdmin(admin.ModelAdmin):
    list_display = ("review", "text", "author", "pk")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "score", "author")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class TitleAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "description", "category", 'pk')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
