from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from versatileimagefield.fields import VersatileImageField
from django.contrib.auth.models import User

# Models for the blog site(Starbuzz-Central)

# The profile model for users on the site

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
# Categories for different kind of stories

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, blank=True, null=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

#  Represent's tags associated with blog posts

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag_articles', args=[self.id])

# The actual post content
STATUS_CHOICES = (('published', 'Published'), ('draft', 'Draft'),)
class Post(models.Model):
    post_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='status', default='draft')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    publication_date = models.DateTimeField(verbose_name='Created')
    picture = VersatileImageField(
        upload_to='blog-uploads/%Y/', height_field='height', width_field='width',
        blank=True,
        null=True,
        verbose_name='Picture as thumbnail'
    )
    height = models.PositiveIntegerField('Profile Image Height', blank=True, null=True)
    width = models.PositiveIntegerField('Profile Image Width', blank=True, null=True)
    picture_description = models.CharField(max_length=127, verbose_name="description of the image", null=False)
    post_excerpt = RichTextField(verbose_name="post excerpt")
    post_content = RichTextUploadingField(null=False, verbose_name="post content")
    is_featured = models.BooleanField(verbose_name="Is the post feature or not?", default=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    views = models.PositiveIntegerField(default=0)

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def date_published(self):
        return self.publication_date.strftime("%B %d, %Y")

    def get_category(self):
        return self.category.title

    def get_article_url(self):
        return reverse('article_details', args=[self.id])
    
    def comment_count(self):
        return self.comments.count()

    def __str__(self):
        return self.title

# Comment section

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


class Advert(models.Model):
    AD_TYPES = (
        ('GIF', 'GIF'),
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
    )
    
    title = models.CharField(max_length=100)
    ad_type = models.CharField(max_length=10, choices=AD_TYPES)
    file = models.FileField(upload_to='advertisements/')
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title