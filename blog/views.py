from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm 
from .models import Post, Comment, Like, Profile
from .forms import PostForm, CustomUserCreationForm , UserUpdateForm, ProfileUpdateForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('post_list')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def post_list(request):
    posts = Post.objects.filter(status='published').order_by('-created_at') 
    return render(request, 'post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Товчлуурын 'name="action"' утгыг шалгах
            action = request.POST.get('action')
            if action == 'publish':
                post.status = 'published'
            else:
                post.status = 'draft'
                
            post.save()
            
            # Хэрэв нийтэлсэн бол нүүр хуудас руу, ноорог бол Stories руу
            if post.status == 'published':
                return redirect('post_list')
            else:
                return redirect('stories')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()
    return render(request, 'post_detail.html', {
        'post': post,
        'is_liked': is_liked
    })

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(post=post, author=request.user, text=text)
    return redirect('post_detail', pk=pk)

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Like моделийн query-г сайжруулах
    like_qs = Like.objects.filter(post=post, user=request.user)
    if like_qs.exists():
        like_qs.delete()
    else:
        Like.objects.create(post=post, user=request.user)
    return redirect('post_detail', pk=pk)

@login_required
def profile(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })

@login_required
def stories_view(request): 
    user_posts = Post.objects.filter(author=request.user)
    drafts = user_posts.filter(status='draft').order_by('-created_at')
    published = user_posts.filter(status='published').order_by('-created_at')
    return render(request, 'stories.html', {'drafts': drafts, 'published': published})
def filter_posts(request):
    cat_id = request.GET.get('category')
    if cat_id:
        posts = Post.objects.filter(category_id=cat_id, status='published')
    else:
        posts = Post.objects.filter(status='published')
    return render(request, 'partials/post_list.html', {'posts': posts})

@login_required
def library_view(request):
    # Хэрэглэгчийн Like дарсан нийтлэлүүдийг харуулах
    liked_posts = [like.post for like in Like.objects.filter(user=request.user).order_by('-created_at')]
    return render(request, 'library.html', {'posts': liked_posts})