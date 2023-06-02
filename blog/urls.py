from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('tag/<int:tag_id>/', views.tag_articles_view, name='tag_articles'),
    path('post/<int:post_id>/', views.article_details, name='article_details'),
    path('categories/', views.categories_view, name='categories'),
    path('contact/', views.contact, name='contact'),
    path('post/<int:post_id>/comment/create/', views.create_comment, name='create_comment'),
]
