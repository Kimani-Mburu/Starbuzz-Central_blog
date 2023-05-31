from django.shortcuts import render
from blog.models import Post, Category

def home_view(request):
    # Get the latest 4 published posts
    latest_posts = Post.objects.filter(status='published').order_by('-publication_date')[:4]

    # Get all categories
    categories = Category.objects.all()

    # Get the most viewed post
    most_viewed_post = Post.objects.filter(status='published').order_by('-views').first()

    # Get the featured post
    featured_post = Post.objects.filter(status='published', is_featured=True).first()

    context = {
        'latest_posts': latest_posts,
        'categories': categories,
        'most_viewed_post': most_viewed_post,
        'featured_post': featured_post,
    }

    return render(request, 'index.html', context)

