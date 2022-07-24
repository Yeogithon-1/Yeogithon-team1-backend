from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('posts/', PostListView.as_view()),
    path('posts/<int:pk>', PostDetailView.as_view()),
    path('posts/<int:pk>/like', PostLikeView.as_view()),
    path('comments/', CommentView.as_view()),
    path('comments/<int:pk>', CommentDetailView.as_view()),
    path('comments/<int:pk>/like', CommentLikeView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
]
