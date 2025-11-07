from django.shortcuts import render, redirect
from posts.models import Post

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
  context = {"posts":posts}
  return render(request, "posts/feeds.html",context)