from cProfile import Profile
from django.shortcuts import render, redirect
from blog.models import Advert, Post, Category, Tag
from django.shortcuts import get_object_or_404
from blog.models import Post
from blog.forms import CommentForm
from django.contrib.auth.decorators import login_required

# Homepage view
def home_view(request):
    # Get the latest 4 published posts
    latest_posts = Post.objects.filter(status='published').order_by('-publication_date')[:4]

    # Get all categories
    categories = Category.objects.all()

    # Get the most viewed post
    most_viewed_post = Post.objects.filter(status='published').order_by('-views')

    # Get the featured post
    featured_posts = Post.objects.filter(status='published', is_featured=True)[:4]

     # Get the latest 3 published posts for the carousel
    carousel_posts = Post.objects.filter(status='published').order_by('-publication_date')[:3]

    # Get the latest 2 published posts for breaking news
    breaking_posts = Post.objects.filter(status='published').order_by('-publication_date')[:2]

    # Get the latest 5 published posts for the featured posts slider
    feature_posts = Post.objects.filter(status='published').order_by('-publication_date')[:5]

    # Get all tags
    tags = Tag.objects.all()

    # Retrieve the latest advertisement
    advert = Advert.objects.latest('created_at')

    all_posts = Post.objects.all()

    #All categories
    categories = Category.objects.all()
    


    context = {
        'latest_posts': latest_posts,
        'categories': categories,
        'most_viewed_post': most_viewed_post,
        'featured_posts': featured_posts,
        'carousel_posts': carousel_posts,
        'breaking_posts': breaking_posts,
        'feature_posts':feature_posts,
        'tags':tags,
        'advert':advert,  
        'all_posts':all_posts,
        'categories':categories
    }

    return render(request, 'index.html', context)

# Create a comment
@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('article_details', post_id=post_id)
    else:
        form = CommentForm()

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'single.html', context)

# Article details view

def article_details(request, post_id):
    # Retrieve the post
    post = get_object_or_404(Post, post_id=post_id)
    #Retrieve the comments
    comments = post.comments.all()
    # Retrieve the latest advertisement
    advert = Advert.objects.latest('created_at')
    #2 Lates posts
    breaking = Post.objects.filter(status='published').order_by('-publication_date')[:2]

    # Get the latest 4 published posts
    latest_posts = Post.objects.filter(status='published').order_by('-publication_date')[:4]

    # Get the latest 3 published posts for the carousel
    carousel_posts = Post.objects.filter(status='published').order_by('-publication_date')[:3]

    # Get all tags
    tags = Tag.objects.all()

    #All categories
    categories = Category.objects.all()

    # Increment the views count for the post
    post.increment_views()

    context = {
        'post': post,
        'comments': comments,
        'advert': advert,
        'breaking':breaking,
        'latest_posts':latest_posts,
        'tags':tags, 
        'carousel_posts':carousel_posts,
        'categories':categories,
    }
    return render(request, 'single.html', context)


def tag_articles_view(request, tag_id):
    # Retrieve the tag based on the tag_id
    tag = get_object_or_404(Tag, id=tag_id)

    # Retrieve the articles associated with the tag
    articles = Post.objects.filter(tags=tag)

    context = {
        'tag': tag,
        'articles': articles
    }

    return render(request, 'category.html', context)


# Category view

def categories_view(request):
    # Retrieve all categories
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'category.html', context)

def contact(request):
    return render(request, 'contact.html')