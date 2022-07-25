from django.shortcuts import get_object_or_404, render
from .serializers import *
from .models import *
from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class MyPostList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)


class PostLikeView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, serializer):
        serializer.save()


class PostListView(views.APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response({'message': '게시글 목록 조회 성공', 'data': serializer.data})

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response({'message': '게시글 작성 성공', 'data': serializer.data})
        return Response({'message': '게시글 작성 실패', 'error': serializer.errors})


class PostDetailView(views.APIView):
    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response({'message': '게시글 상세 조회 성공', 'data': serializer.data})

    def put(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '게시글 수정 성공', 'data': serializer.data})
        return Response({'message': '게시글 수정 실패', 'error': serializer.errors})

    def delete(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response({'message': '게시글 삭제 성공'})


class PostSearchView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(comment__content__icontains=query)
            ).distinct()
        return queryset_list


class CommentLikeView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, serializer):
        serializer.save()


class CommentView(views.APIView):
    def post(self, request, format=None):
        serializer = CommentDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '댓글 작성 성공', 'data': serializer.data})
        return Response({'message': '댓글 작성 실패', 'error': serializer.errors})

    def get(self, request, format=None):
        comments = Comment.objects.filter(parent=None)
        serializer = CommentDetailSerializer(comments, many=True)
        return Response(serializer.data)


class CommentDetailView(views.APIView):
    def get(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentDetailSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': '댓글 수정 성공', 'data': serializer.data})
        return Response({'message': '댓글 수정 실패', 'error': serializer.errors})

    def delete(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response()


class SignUpView(views.APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공', 'data': serializer.data})
        return Response({'message': '회원가입 실패', 'error': serializer.errors})


class LoginView(views.APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response({'message': "로그인 성공", 'data': serializer.data})
        return Response({'message': "로그인 실패", 'data': serializer.errors})
