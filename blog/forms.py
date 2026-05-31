from django import forms
from .models import Post, Category, Tag, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "tags",
            "featured_image",
            "content",
            "excerpt",
            "status",
            "is_featured",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter post title"}
            ),
            "category": forms.Select(
                attrs={"class": "form-control"},
            ),
            "tags": forms.SelectMultiple(
                attrs={"class": "form-control"},
            ),
            "featured_image": forms.FileInput(
                attrs={"class": "form-control"},
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Write your content here...",
                }
            ),
            "excerpt": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Brief description of the post",
                }
            ),
            "status": forms.Select(
                attrs={"class": "form-control"},
            ),
            "is_featured": forms.CheckboxInput(
                attrs={"class": "form-check-input"},
            ),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Category name"}
            ),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Tag name"}
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "your@email.com",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your comment...",
                }
            ),
        }


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your name"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "your@email.com"}
        ),
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Subject"}
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Your message...",
            }
        ),
    )
