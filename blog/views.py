from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment
from .forms import BlogForm, CommentForm
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from .forms import BlogForm

def home(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def login_view(request):
    if request.method == 'POST':
        username_email = request.POST.get('username_email')
        password = request.POST.get('password')
        user = authenticate(request, username=username_email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'blog/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the home page after logout

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

def create_user(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
        else:
            # Check if email is already registered
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken. Please choose another.')
            else:
                # Create the user
                user = User.objects.create_user(email=email, username=email, password=password)
                user.first_name = full_name
                user.save()
                messages.success(request, 'Account created successfully. You can now login.')
                return redirect('login')
    return render(request, 'blog/create.html')
@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new Blog instance but don't save it yet
            blog = form.save(commit=False)
            blog.author = request.user  # Assign the current logged-in user as the author
            blog.save()  # Now save the blog with the author assigned
            return redirect('blog_detail', pk=blog.pk)  # Redirect to the detail page of the created blog
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/blog_detail.html', {'blog': blog})
@login_required
def edit_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', pk=blog.pk)  # Redirect to the blog detail page
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/edit_blog.html', {'form': form, 'blog': blog})
@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')  # Redirect to a view that lists all blogs
    return render(request, 'blog/delete_blog.html', {'blog': blog})
def blog_list(request):
    # Fetch all blog posts from the database
    blogs = Blog.objects.all()

    # Render the template with the list of blogs
    return render(request, 'blog/blog_list.html', {'blogs': blogs})