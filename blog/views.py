from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from blog.models import Advert, Comment, Post, Category, SearchHistory, Tag, Profile
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q 
from django.shortcuts import get_object_or_404
from blog.models import Post
from blog.forms import CommentForm, ProfileUpdateForm
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

# Article details view
@login_required(login_url='blog:login')  # Require login for posting comments
def article_details(request, post_id):
    # Retrieve the post
    post = get_object_or_404(Post, post_id=post_id)

    # Retrieve the comments
    comments = Comment.objects.filter(post=post)

    # Retrieve the latest advertisement
    advert = Advert.objects.latest('created_at')

    # 2 Latest posts
    breaking = Post.objects.filter(status='published').order_by('-publication_date')[:2]

    # Get the latest 4 published posts
    latest_posts = Post.objects.filter(status='published').order_by('-publication_date')[:4]

    # Get the latest 3 published posts for the carousel
    carousel_posts = Post.objects.filter(status='published').order_by('-publication_date')[:3]

    # Get all tags
    tags = Tag.objects.all()

    # All categories
    categories = Category.objects.all()

    # Increment the views count for the post
    post.increment_views()

    # Handle comment submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:  # Check if user is logged in
                comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog:article_details', post_id=post_id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'advert': advert,
        'breaking': breaking,
        'latest_posts': latest_posts,
        'tags': tags,
        'carousel_posts': carousel_posts,
        'categories': categories,
        'form': form
    }
    return render(request, 'single.html', context)


def tag_articles_view(request, id):
    # Retrieve the tag based on the tag_id
    tag = get_object_or_404(Tag, id=id)

    # Retrieve the articles associated with the tag
    articles = Post.objects.filter(tags=tag)

    # Retrieve the latest advertisement
    advert = Advert.objects.latest('created_at')

    # Get the latest 4 published posts
    latest_posts = Post.objects.filter(status='published').order_by('-publication_date')[:4]

    # Get the latest 3 published posts for the carousel
    carousel_posts = Post.objects.filter(status='published').order_by('-publication_date')[:3]

    # All categories
    categories = Category.objects.all()

    context = {
        'tag': tag,
        'articles': articles,
        'advert':advert,
        'latest_posts':latest_posts,
        'carousel_posts':carousel_posts,
        'categories':categories
    }

    return render(request, 'tag_articles.html', context)


# Category view

def categories_view(request):
    # Retrieve all categories
    categories = Category.objects.all()

    # Retrieve the latest advertisement
    advert = Advert.objects.latest('created_at')

    # Get the latest 4 published posts
    latest_posts = Post.objects.filter(status='published').order_by('-publication_date')[:4]

    # Get all tags
    tags = Tag.objects.all()

    context = {
        'categories': categories,
        'advert':advert,
        'latest_posts':latest_posts,
        'tags':tags
    }

    return render(request, 'category.html', context)

def contact(request):
    return render(request, 'contact.html')

# profile view
@login_required

def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    
    # Get the latest 3 published posts for the carousel
    carousel_posts = Post.objects.filter(status='published').order_by('-publication_date')[:3]

    # All categories
    categories = Category.objects.all()
    
    context = {
        'profile': profile,
        'carousel_posts':carousel_posts,
        'categories':categories
        }
    return render(request, 'profile.html', context)

# Update profile

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileUpdateForm()
        return render(request, 'accounts/profile_update.html', {'form': form})

    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            profile = request.user.profile
            profile.bio = form.cleaned_data['bio']
            profile.website = form.cleaned_data['website']
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
            profile.save()
            return redirect('blog:profile')  # Update the redirect URL
        return render(request, 'profile_update.html', {'form': form})
# Search view

def search_results_view(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')

        # Query the posts that contain the keyword in either the title or content
        posts = Post.objects.filter(Q(title__icontains=keyword) | Q(post_content__icontains=keyword))

        # Record the search history for the authenticated user
        SearchHistory.objects.create(user=request.user, query=keyword)

    else:
        # Handle anonymous user search history
        keyword = request.GET.get('keyword')
        posts = Post.objects.none()  # Return an empty queryset initially

        if keyword:
            posts = Post.objects.filter(Q(title__icontains=keyword) | Q(post_content__icontains=keyword))

            # Record the search history for anonymous user
            SearchHistory.objects.create(user=None, query=keyword)

    # Get the latest 3 published posts for the carousel
    carousel_posts = Post.objects.filter(status='published').order_by('-publication_date')[:3]

    # All categories
    categories = Category.objects.all()

    context = {
        'keyword': keyword,
        'posts': posts,
        'carousel_posts': carousel_posts,
        'categories': categories
    }
    return render(request, 'search.html', context)

# Account signup view

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('blog:login')  # Replace 'blog:profile' with the URL name of your profile page

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)

        # Create profile for the user
        profile = Profile.objects.create(user=user)

        return response
    
# login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog:home')  
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('blog:home') 