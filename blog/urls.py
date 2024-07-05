# blog/urls.py

from django.urls import path
from .views import home, post_detail, about, contact, login_view, create_post, create_user, create_blog, blog_detail, edit_blog, delete_blog,blog_list
from . import views
urlpatterns = [
    path('', home, name='home'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', login_view, name='login'),
    path('create/', create_post, name='create_post'),
    path('create_user/', create_user, name='create_user'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:pk>/edit/', views.edit_blog, name='edit_blog'),
    path('blog/<int:pk>/delete/', views.delete_blog, name='delete_blog'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('logout/', views.logout_view, name='logout'),

]
