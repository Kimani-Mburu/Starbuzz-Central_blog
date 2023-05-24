import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Profile, Category, Tag, Post, Comment

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ("id", "user", "bio", "profile_image")

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")

class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ("id", "name")

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "post", "author", "content", "created_at")

class PostType(DjangoObjectType):
    comments = graphene.List(CommentType)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "subtitle",
            "slug",
            "body",
            "meta_description",
            "date_created",
            "date_modified",
            "publish_date",
            "published",
            "author",
            "tags",
            "comments",
        )

    def resolve_comments(self, info):
        return self.comments.all()

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    profiles = graphene.List(ProfileType)
    categories = graphene.List(CategoryType)
    tags = graphene.List(TagType)
    posts = graphene.List(PostType)

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_profiles(self, info):
        return Profile.objects.all()

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_tags(self, info):
        return Tag.objects.all()

    def resolve_posts(self, info):
        return Post.objects.all()

schema = graphene.Schema(query=Query)
