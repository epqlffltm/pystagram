from django.shortcuts import render, redirect
from posts.models import Post

def feeds(request):
    if not request.user.is_authenticated:
        return redirect("/users/login")
    user=request.user
    is_authenticated = user.is_authenticated
    print("user:", user)
    print("is_authenticated:", is_authenticated)
    posts=Post.objects.all()
    context={"posts":posts}
    return render(request,"posts/feeds.html", context)