from django.contrib import admin
from django.db.models import Count
from blog.models import Advert, Profile, Post, SearchHistory, Tag, Comment, Category


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
        "views",
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


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ['title', 'ad_type', 'link']
    list_filter = ['ad_type']

class TopSearchKeywordFilter(admin.SimpleListFilter):
    title = 'Top Search Keywords'
    parameter_name = 'top_search_keyword'

    def lookups(self, request, model_admin):
        top_keywords = SearchHistory.objects.values('query').annotate(count=Count('query')).order_by('-count')[:5]
        return [(kw['query'], kw['query']) for kw in top_keywords]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(keyword=self.value())
        return queryset

class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'timestamp')
    list_filter = (TopSearchKeywordFilter, 'user', 'timestamp')

admin.site.register(SearchHistory, SearchHistoryAdmin)