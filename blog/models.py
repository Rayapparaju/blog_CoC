from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


def unique_slugify(instance, value, fallback="item"):
    slug = slugify(value) or fallback
    model = instance.__class__
    origin_slug = slug
    counter = 1
    while model.objects.filter(slug=slug).exclude(id=instance.id).exists():
        slug = f"{origin_slug}-{counter}"
        counter += 1
    return slug


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name, "category")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name, "tag")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    featured_image = models.ImageField(
        upload_to="blog_images/", blank=True, null=True
    )
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title, "post")
        if not self.excerpt:
            self.excerpt = self.content[:200]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
