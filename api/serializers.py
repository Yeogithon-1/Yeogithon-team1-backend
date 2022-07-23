from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author',
                  'content', 'like', 'created_at', 'parent', 'reply_count']

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author']

    def update(self, instance, validated_data):
        user = validated_data.pop('author', None)
        if user in instance.like.all():
            instance.like.remove(user)
        else:
            instance.like.add(user)
        instance.save()
        return instance


class CommentChildSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'parent', 'author',
                  'content', 'like', 'like_count', 'created_at']

    def get_like_count(self, obj):
        return obj.like.count()


class CommentDetailSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'content', 'like', 'like_count', 'created_at', 'replies'
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_like_count(self, obj):
        return obj.like.count()


class PostSerializer(serializers.ModelSerializer):
    comment = CommentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'content',
                  'created_at', 'tag', 'comment']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'], username=validated_data['username'],)
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):  # 유효성 검사가 끝나지 않은 데이터니까 validated_data가 아닌 그냥 data를 가져옴
        email = data.get("email", None)
        password = data.get("password", None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError()
            else:
                return user
        else:
            raise serializers.ValidationError()
