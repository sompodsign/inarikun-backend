from django.db import models
from django.urls import reverse
from django.utils import timezone

from core.models import UUIDMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(UUIDMixin):
    """
    Category model
    * Represent a category of blog posts
    * Has a name
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Topic(UUIDMixin):
    """
    Topic model
    * Represent a topic of a category
    * Has a name
    """
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Article(UUIDMixin):
    """
    Post model
    * Represent a blog post in a topic
    * Has a title and a body
    * Has a content (markdown)
    * Has an author (User)
    * Has a topic (optional)
    * Has a created_at timestamp
    * Has an updated_at (auto_now)
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now())
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')

    def get_absolute_url(self):
        return reverse('article:detail', args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ])

    def __str__(self):
        return self.title


class ArticleTag(models.Model):
    name = models.CharField(max_length=30)
    article = models.ManyToManyField(Article, related_name='articletag_set')

    def __str__(self):
        return self.name


class PostImage(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/images/')


class Comment(UUIDMixin):
    """
    Comment model
    * Represent a comment on a post
    """
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.body


class CommentImage(models.Model):
    """
    CommentImage model (for comment images)
    """
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    path = models.ImageField(upload_to='blog/images/')

    def __str__(self):
        return self.path

