from django.shortcuts import render, redirect

from posts.forms import CommentForm
from posts.models import Post
from django.views.decorators.http import require_POST

def feeds(request):
    if not request.user.is_authenticated:
        return redirect("/users/login")
    user=request.user
    is_authenticated = user.is_authenticated
    print("user:", user)
    print("is_authenticated:", is_authenticated)
    posts=Post.objects.all()
    comment_form=CommentForm()
    context={"posts":posts,"comment_form":comment_form,}
    return render(request,"posts/feeds.html", context)

@require_POST
def comment_add(request):
    print(request.POST)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()
        print(comment.id)
        print(comment.content)
        print(comment.user)

    return redirect("/posts/feeds/")