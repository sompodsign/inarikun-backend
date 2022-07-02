from django.db import models
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


class Post(UUIDMixin):
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
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/images/')


class Comment(UUIDMixin):
    """
    Comment model
    * Represent a comment on a post
    """
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

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

