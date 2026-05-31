from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Post, Category, Tag, Comment
from .forms import (
    PostForm,
    CategoryForm,
    TagForm,
    CommentForm,
    ContactForm,
)

# --- Public Views ---


def home(request):
    featured_posts = Post.objects.filter(status="published", is_featured=True)[:3]
    recent_posts = Post.objects.filter(status="published")[:6]
    categories = Category.objects.all()
    authors = User.objects.filter(posts__status="published").distinct().count()
    context = {
        "featured_posts": featured_posts,
        "recent_posts": recent_posts,
        "categories": categories,
        "total_posts_count": Post.objects.filter(status="published").count(),
        "total_authors": authors,
    }
    return render(request, "home.html", context)


def blog_list(request):
    posts = Post.objects.filter(status="published")
    paginator = Paginator(posts, 6)
    page = request.GET.get("page")
    posts = paginator.get_page(page)
    return render(request, "blog_list.html", {"posts": posts})


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    comments = post.comments.filter(is_approved=True)
    recent_posts = (
        Post.objects.filter(status="published")
        .exclude(id=post.id)
        .order_by("-created_at")[:3]
    )

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(
                request, "Your comment has been submitted and is awaiting approval."
            )
            return redirect("blog_detail", slug=post.slug)
    else:
        form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "recent_posts": recent_posts,
        "form": form,
    }
    return render(request, "blog_detail.html", context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status="published")
    paginator = Paginator(posts, 6)
    page = request.GET.get("page")
    posts = paginator.get_page(page)
    return render(
        request, "category_posts.html", {"category": category, "posts": posts}
    )


def search_posts(request):
    query = request.GET.get("q", "")
    posts = Post.objects.filter(status="published").filter(
        Q(title__icontains=query)
        | Q(content__icontains=query)
        | Q(category__name__icontains=query)
        | Q(tags__name__icontains=query)
    ).distinct()
    paginator = Paginator(posts, 6)
    page = request.GET.get("page")
    posts = paginator.get_page(page)
    return render(
        request, "search_results.html", {"posts": posts, "query": query}
    )


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(
                request,
                "Your message has been sent successfully! We will get back to you soon.",
            )
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


# --- Admin Authentication ---


def admin_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials or not authorized.")
    return render(request, "admin/login.html")


def admin_logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("admin_login")


# --- Admin Dashboard ---


@login_required(login_url="admin_login")
def dashboard(request):
    total_posts = Post.objects.count()
    total_published = Post.objects.filter(status="published").count()
    total_drafts = Post.objects.filter(status="draft").count()
    total_categories = Category.objects.count()
    total_tags = Tag.objects.count()
    total_comments = Comment.objects.count()
    pending_comments = Comment.objects.filter(is_approved=False).count()
    recent_posts = Post.objects.order_by("-created_at")[:5]
    recent_comments = Comment.objects.order_by("-created_at")[:5]

    context = {
        "total_posts": total_posts,
        "total_published": total_published,
        "total_drafts": total_drafts,
        "total_categories": total_categories,
        "total_tags": total_tags,
        "total_comments": total_comments,
        "pending_comments": pending_comments,
        "recent_posts": recent_posts,
        "recent_comments": recent_comments,
    }
    return render(request, "admin/dashboard.html", context)


# --- Post Management ---


@login_required(login_url="admin_login")
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "admin/post_list.html", {"posts": posts})


@login_required(login_url="admin_login")
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, "Post created successfully!")
            return redirect("post_list")
    else:
        form = PostForm()
    return render(request, "admin/post_form.html", {"form": form, "edit": False})


@login_required(login_url="admin_login")
def post_edit(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        messages.error(request, "Post not found.")
        return redirect("post_list")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect("post_list")
    else:
        form = PostForm(instance=post)
    return render(
        request, "admin/post_form.html", {"form": form, "edit": True, "post": post}
    )


@login_required(login_url="admin_login")
def post_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        messages.error(request, "Post not found.")
        return redirect("post_list")
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect("post_list")
    return render(request, "admin/post_confirm_delete.html", {"post": post})


# --- Category Management ---


@login_required(login_url="admin_login")
def category_list(request):
    categories = Category.objects.all().order_by("name")
    return render(
        request, "admin/category_list.html", {"categories": categories}
    )


@login_required(login_url="admin_login")
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully!")
            return redirect("category_list")
    else:
        form = CategoryForm()
    return render(
        request, "admin/category_form.html", {"form": form, "edit": False}
    )


@login_required(login_url="admin_login")
def category_edit(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect("category_list")
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)
    return render(
        request,
        "admin/category_form.html",
        {"form": form, "edit": True, "category": category},
    )


@login_required(login_url="admin_login")
def category_delete(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect("category_list")
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect("category_list")
    return render(
        request, "admin/category_confirm_delete.html", {"category": category}
    )


# --- Tag Management ---


@login_required(login_url="admin_login")
def tag_list(request):
    tags = Tag.objects.all().order_by("name")
    return render(request, "admin/tag_list.html", {"tags": tags})


@login_required(login_url="admin_login")
def tag_create(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tag created successfully!")
            return redirect("tag_list")
    else:
        form = TagForm()
    return render(request, "admin/tag_form.html", {"form": form, "edit": False})


@login_required(login_url="admin_login")
def tag_edit(request, pk):
    try:
        tag = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        messages.error(request, "Tag not found.")
        return redirect("tag_list")
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, "Tag updated successfully!")
            return redirect("tag_list")
    else:
        form = TagForm(instance=tag)
    return render(
        request, "admin/tag_form.html", {"form": form, "edit": True, "tag": tag}
    )


@login_required(login_url="admin_login")
def tag_delete(request, pk):
    try:
        tag = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        messages.error(request, "Tag not found.")
        return redirect("tag_list")
    if request.method == "POST":
        tag.delete()
        messages.success(request, "Tag deleted successfully!")
        return redirect("tag_list")
    return render(request, "admin/tag_confirm_delete.html", {"tag": tag})


# --- Comment Management ---


@login_required(login_url="admin_login")
def comment_list(request):
    comments = Comment.objects.all().order_by("-created_at")
    return render(
        request, "admin/comment_list.html", {"comments": comments}
    )


@login_required(login_url="admin_login")
def comment_approve(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        messages.error(request, "Comment not found.")
        return redirect("comment_list")
    comment.is_approved = True
    comment.save()
    messages.success(request, "Comment approved!")
    return redirect("comment_list")


@login_required(login_url="admin_login")
def comment_reject(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        messages.error(request, "Comment not found.")
        return redirect("comment_list")
    comment.is_approved = False
    comment.save()
    messages.success(request, "Comment rejected!")
    return redirect("comment_list")


@login_required(login_url="admin_login")
def comment_delete(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        messages.error(request, "Comment not found.")
        return redirect("comment_list")
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
        return redirect("comment_list")
    return render(
        request, "admin/comment_confirm_delete.html", {"comment": comment}
    )


# --- Profile ---


@login_required(login_url="admin_login")
def profile(request):
    return render(request, "admin/profile.html")
