from django.contrib import admin

from blog.models import Profile, Post, Tag, Comment, Category


# Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile

# Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag

# Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = (
        "id",
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
    )
    list_filter = (
        "published",
        "publish_date",
    )
    list_editable = (
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
    )
    search_fields = (
        "title",
        "subtitle",
        "slug",
        "body",
    )
    prepopulated_fields = {
        "slug": (
            "title",
            "subtitle",
        )
    }
    date_hierarchy = "publish_date"
    save_on_top = True

#Comment model

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment