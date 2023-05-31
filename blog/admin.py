from django.contrib import admin
from blog.models import Profile, Post, Tag, Comment, Category


# Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile


# Categories model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


# Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


# Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = (
        "post_id",
        "title",
        "slug",
        "status",
        "category",
        "publication_date",
        "is_featured",
    )
    list_filter = (
        "status",
        "category",
        "publication_date",
        "is_featured",
    )
    list_editable = (
        "title",
        "slug",
        "status",
        "category",
        "publication_date",
        "is_featured",
    )
    search_fields = (
        "title",
        "slug",
        "post_content",
    )
    prepopulated_fields = {
        "slug": ("title",)
    }
    date_hierarchy = "publication_date"


# Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
