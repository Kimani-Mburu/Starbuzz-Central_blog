from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('tag/<int:tag_id>/', views.tag_articles_view, name='tag_articles'),
    path('article/<int:post_id>/', views.article_detail, name='article_details'),
    path('post/<int:pk>/comment/', views.create_comment, name='post_comment'),
]
