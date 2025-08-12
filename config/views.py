from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        return redirect("/posts/feeds")
    elif not request.user.is_authenticated:
        return redirect("/users/login")  # ← 여기만 수정

    return render(request, 'index.html')  # 실제로는 도달하지 않음
