from django.shortcuts import render, redirect

def feeds(request):
    if not request.user.is_authenticated:
        return redirect("/users/login")
    user=request.user
    is_authenticated = user.is_authenticated
    print("user:", user)
    print("is_authenticated:", is_authenticated)
    return render(request,"posts/feeds.html")