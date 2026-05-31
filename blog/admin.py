from django.contrib import admin
from .models import Post, Category, Tag, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "title",
        "author",
        "category",
        "status",
        "is_featured",
        "created_at",
    )
    list_filter = ("status", "is_featured", "category", "created_at")
    search_fields = ("title", "content", "excerpt")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    filter_horizontal = ("tags",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "post", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("name", "email", "message")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    approve_comments.short_description = "Approve selected comments"
