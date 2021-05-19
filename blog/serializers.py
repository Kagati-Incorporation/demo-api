from rest_framework import serializers

from .models import (
    BlogCategory,
    Article,
)


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'
        read_only_fields = ('slug',)


class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.title', read_only=True)
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    author_email = serializers.CharField(source='author.email', read_only=True)
    class Meta:
        model = Article
        exclude = (
            'modified_on',
            'created_on',
        )
        read_only_fields = ('slug', 'author', 'views')
