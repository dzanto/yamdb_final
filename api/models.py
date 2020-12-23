from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    slug = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['-id']


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    slug = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['-id']


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    year = models.PositiveIntegerField(
        verbose_name='Year',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.date.today().year)
        ]
    )
    description = models.TextField(verbose_name='Description')
    genre = models.ManyToManyField(Genre, verbose_name='Genre')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles", null=True,
        verbose_name='Category'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Review(models.Model):
    text = models.TextField()
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(10, message="cool")]
    )
    title = models.ForeignKey(
        Title, blank=True, on_delete=models.CASCADE,
        related_name="reviews"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="review_author"
    )
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
