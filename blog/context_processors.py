from .models import Category, Post


def common_context(request):
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(status="published")[:3]
    return {
        "categories": categories,
        "recent_posts": recent_posts,
    }
