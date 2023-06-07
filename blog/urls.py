from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.SignupView.as_view(), name='account_signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tag/<int:id>/', views.tag_articles_view, name='tag_articles'),
    path('post/<int:post_id>/', views.article_details, name='article_details'),
    path('categories/', views.categories_view, name='categories'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('search/', views.search_results_view, name='search_results'),


]
