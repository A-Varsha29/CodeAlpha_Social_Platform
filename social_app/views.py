from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Post, Comment

def home(request):
    if request.method == 'POST':
        # 1. Handle Like Button Submission
        if 'submit_like' in request.POST:
            post_id = request.POST.get('post_id')
            if post_id:
                target_post = Post.objects.get(id=post_id)
                # If the logged-in user already liked it, remove it. Otherwise, add it.
                if request.user in target_post.likes.all():
                    target_post.likes.remove(request.user)
                else:
                    target_post.likes.add(request.user)
                return redirect('home')

        # 2. Handle Comment Submission
        elif 'submit_comment' in request.POST:
            comment_text = request.POST.get('comment_content')
            post_id = request.POST.get('post_id')
            
            if comment_text and post_id:
                target_post = Post.objects.get(id=post_id)
                Comment.objects.create(post=target_post, author=request.user, content=comment_text)
                return redirect('home')
        
        # 3. Handle Normal Post Submission
        else:
            post_content = request.POST.get('content')
            if post_content:
                Post.objects.create(author=request.user, content=post_content)
                return redirect('home')

    # Fetch posts along with comments and pre-calculated likes count
    posts = Post.objects.all().prefetch_related('comments', 'likes').order_by('-created_at')
    return render(request, 'social_app/home.html', {'posts': posts})

def user_profile(request, username):
    # Fetch the specific user based on the username in the URL
    profile_user = get_object_or_404(User, username=username)
    
    # Filter and fetch only the posts created by this specific user
    profile_posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    
    return render(request, 'social_app/profile.html', {
        'profile_user': profile_user,
        'profile_posts': profile_posts
    })