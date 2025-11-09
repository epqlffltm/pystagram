from django.shortcuts import render, redirect
from posts.models import Post, Comment, PostImage, HashTag
from posts.forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

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
    return redirect("users:login")
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
        if request.GET.get("next"):
          url_next = request.GET.get("next")
          print(comment.id)
          print(comment.content)
          print(comment.user)
        #return HttpResponseRedirect(f"/posts/feeds/#post-{comment.post.id}")
        else:
          url_next = reverse("posts:feeds") + f"#post-{comment.post.id}"
        return HttpResponseRedirect(url_next)
  
@require_POST
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        post_id = comment.post.id  # ✅ 삭제 전에 저장
        comment.delete()
        #return HttpResponseRedirect(f"/posts/feeds/#post-{post_id}")
        url = reverse("posts:feeds") + f"#post-{comment.post.id}"
        return HttpResponseRedirect(url)
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
              #"image"에 전달된 여러장의 이미지 파일로 각각의 포스트 이미지 생성
                PostImage.objects.create(post=post, photo=image_file)
                tag_string = request.POST.get("tags")
                if tag_string:
                  tag_names = [tag_name.strip() for tag_name in tag_string.split(",")]
                  for tag_name in tag_names:
                    tag, _ = HashTag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)
                    #get_of_create로 생성하거나 가저온 HashTag 객체를 post의tags에 추가한다.
            #return HttpResponseRedirect(f"/posts/feeds/#post-{post.id}")
            url = reverse("posts:feeds") + f"#post-{post.id}"
            return HttpResponseRedirect(url)

    else:
        form = PostForm()

    context = {
        "form": form,
        "user": request.user,
    }
    return render(request, "posts/post_add.html", context)

def tags(request, tag_name):
  try:
    tag = HashTag.objects.get(name=tag_name)
    print(tag)
  except HashTag.DoesNotExist:
    posts = Post.objects.none()
    #tag_name에 해당하는 HashTag를 찾지 못한다면 빈 query set을 돌려준다
  else:
    posts = Post.objects.filter(tags=tag)
    #tags에 찾은 HashTag 객체들을 필터
    comment_form = CommentForm()
  context = {
    "tag_name":tag_name,
    "posts":posts,
    "comment_from":comment_form
  }
  #context로 Template에 필터링된 post query set을 념겨주며, 어떤 tag_name로 검색했는지도 념겨준다.
  return render(request,"posts/tags.html", context)

def post_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  context = {"post":post}
  return render(request, "posts/post_detail.html", context)