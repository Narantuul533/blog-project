from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('signup/', views.signup, name='signup'),
    path('post/new/', views.post_create, name='post_create'),
    path('filter-posts/', views.filter_posts, name='filter_posts'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('stories/', views.stories_view, name='stories'),
    path('library/', views.library_view, name='library'),
]