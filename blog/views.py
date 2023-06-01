from django.shortcuts import render, redirect
from blog.models import Post, Category
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

# Create a comment

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
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
    return render(request, 'create_comment.html', context)

# Article details view

def article_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'single.html', context)
