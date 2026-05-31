from django.urls import path
from . import views

urlpatterns = [
    # Public
    path("", views.home, name="home"),
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("category/<slug:slug>/", views.category_posts, name="category_posts"),
    path("search/", views.search_posts, name="search_posts"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    # Admin Auth
    path("admin-panel/login/", views.admin_login, name="admin_login"),
    path("admin-panel/logout/", views.admin_logout_view, name="admin_logout"),
    # Admin Dashboard
    path("admin-panel/", views.dashboard, name="dashboard"),
    # Post Management
    path("admin-panel/posts/", views.post_list, name="post_list"),
    path("admin-panel/posts/create/", views.post_create, name="post_create"),
    path("admin-panel/posts/<int:pk>/edit/", views.post_edit, name="post_edit"),
    path(
        "admin-panel/posts/<int:pk>/delete/",
        views.post_delete,
        name="post_delete",
    ),
    # Category Management
    path("admin-panel/categories/", views.category_list, name="category_list"),
    path(
        "admin-panel/categories/create/",
        views.category_create,
        name="category_create",
    ),
    path(
        "admin-panel/categories/<int:pk>/edit/",
        views.category_edit,
        name="category_edit",
    ),
    path(
        "admin-panel/categories/<int:pk>/delete/",
        views.category_delete,
        name="category_delete",
    ),
    # Tag Management
    path("admin-panel/tags/", views.tag_list, name="tag_list"),
    path("admin-panel/tags/create/", views.tag_create, name="tag_create"),
    path("admin-panel/tags/<int:pk>/edit/", views.tag_edit, name="tag_edit"),
    path(
        "admin-panel/tags/<int:pk>/delete/", views.tag_delete, name="tag_delete"
    ),
    # Comment Management
    path("admin-panel/comments/", views.comment_list, name="comment_list"),
    path(
        "admin-panel/comments/<int:pk>/approve/",
        views.comment_approve,
        name="comment_approve",
    ),
    path(
        "admin-panel/comments/<int:pk>/reject/",
        views.comment_reject,
        name="comment_reject",
    ),
    path(
        "admin-panel/comments/<int:pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    # Profile
    path("admin-panel/profile/", views.profile, name="profile"),
]
