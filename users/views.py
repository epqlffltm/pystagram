from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm, SignupForm
from users.models import User

def login_view(request):
  #이미 로그인했다면
  if request.user.is_authenticated:
    return redirect("posts:feeds")
  
  if request.method == "POST":
    #LoginForm인트턴스 생성, 입력 데이터는request.post를 사용
    form = LoginForm(data=request.POST)
    if form.is_valid():
      username=form.cleaned_data["username"]
      password=form.cleaned_data["password"]
      print("form.is_valid(): ",form.is_valid())
      #LoginForm에 들어온 데이터가 적절한지 유효성 검사
      
      
      user=authenticate(username=username, password=password)
      #username, userpassword에 해당하는 사용자가 있는지 검사
      
      if user:
        login(request,user)
        return redirect("posts:feeds")
      #로그인 처리 후 피트 페이지로 redirect
      
      else:
        print("로그인에 실패했습니다")
        form.add_error(None,"입력한 자격증명에 해당하는 사용자가 없습니다.")
        
    # print("form.cleaned_data: ",form.cleaned_data)#생성한 LoginForm인스턴스를 템플릿에 "form"이라는 키로 전달한다.
    context = {"form":form}
    return render(request,"users/login.html",context)
  
  else:
    form=LoginForm()
    context = {"form": form}
    return render(request, "users/login.html",context)
  
def logout_view(request):
  logout(request)
    
  return redirect("users:login")

def signup(request):
  if request.method == "POST":
    form = SignupForm(data=request.POST, files=request.FILES)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data["username"]
      password1 = form.cleaned_data["password1"]
      password2 = form.cleaned_data["password2"]
      profile_image = form.cleaned_data["profile_image"]
      short_description = form.cleaned_data["short_description"]
      print(username)
      print(password1,password2)
      print(profile_image)
      print(short_description)
      if password1 !=password2:
        form.add_error("password2","비밀번호와 비밀번호 확인란의 값이 다릅니다")
      if User.objects.filter(username=username).exists():
        form.add_error("username","입력한 사용자명은 이미 사용중입니다.")
      if form.errors:
        context = {"form":form}
        return render(request, "users/signup.html",context)
      #에러가 없다면, 사용자를 생성하고 로그인 처리 후 피트 페이지로 이동
      else:
        user = User.objects.create_user(
          username=username,
          password=password1,
          profile_image=profile_image,
          short_description=short_description,
        )
        login(request, user)
        return redirect("posts:feeds")
    print(request.POST)
    print(request.FILES)
    #context = {"form":form}
    #return render(request, "users/signup.html",context)
    
  form = SignupForm()
  context = {"form": form}
  return render(request, "users/signup.html", context)
  
  #LoginForm인트턴스 생성
  #form=LoginForm()
  #생성한 LoginForm인스턴스를 템플릿에 "form"이라는 키로 전달한다.
  #context={"form":form,}
  #return render(request, "users/login.html",context)