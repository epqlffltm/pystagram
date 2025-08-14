from django.urls import path
from users.views import login_view, logout_view, signup

urlpatterns = [
    path('login/', login_view, name='login'),      # name 인자 추가
    path('logout/', logout_view, name='logout'),  # name 인자 추가
    path('signup/', signup, name='signup'),      # name 인자 추가
]