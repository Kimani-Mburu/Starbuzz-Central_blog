from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('post/<int:pk>/', views.article_details, name='post_detail'),
    path('post/<int:pk>/comment/', views.create_comment, name='post_comment'),
]
