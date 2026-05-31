from django import template
from ..models import Category, Tag, Post

register = template.Library()


@register.inclusion_tag("navbar.html", takes_context=True)
def navbar(context):
    request = context["request"]
    categories = Category.objects.all()
    return {
        "categories": categories,
        "request": request,
    }


@register.inclusion_tag("footer.html", takes_context=True)
def footer(context):
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(status="published")[:3]
    return {
        "categories": categories,
        "recent_posts": recent_posts,
    }


@register.simple_tag
def total_posts():
    return Post.objects.filter(status="published").count()


@register.simple_tag
def total_categories():
    return Category.objects.count()


@register.simple_tag
def total_tags():
    return Tag.objects.count()
