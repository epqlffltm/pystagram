from django.shortcuts import render, redirect
from posts.models import Post, Comment, PostImage
from posts.forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseForbidden

def feeds(request):
  #요청(request)으로부터 사용자 정보를 가저온다.
  user = request.user
  
  #가저온 사용자가 로그인 했는지 여부를 가저온다.
  is_authenticated = user.is_authenticated
  
  print("user: ",user)
  print("is_authenticated: ", is_authenticated)
  
  #사용자가 로그인을 안한 경우
  if not request.user.is_authenticated:
    #/users/login으로 url로 이동시킴
    return redirect("/users/login/")
  posts = Post.objects.all()
  comment_form = CommentForm()
  context = {
    "posts":posts,
    "comment_form":comment_form,
    }
  return render(request, "posts/feeds.html",context)

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
        return HttpResponseRedirect(f"/posts/feeds/#post-{comment.post.id}")
  
@require_POST
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        post_id = comment.post.id  # ✅ 삭제 전에 저장
        comment.delete()
        return HttpResponseRedirect(f"/posts/feeds/#post-{post_id}")
    else:
        return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다.")

    
def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            for image_file in request.FILES.getlist("images"):
                PostImage.objects.create(post=post, photo=image_file)

            return HttpResponseRedirect(f"/posts/feeds/#post-{post.id}")

    else:
        form = PostForm()

    context = {
        "form": form,
        "user": request.user,
    }
    return render(request, "posts/post_add.html", context)

