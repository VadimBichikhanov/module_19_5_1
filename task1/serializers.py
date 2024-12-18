from rest_framework import serializers
from .models import Buyer, Game, News, OtherModel, Article
from django.contrib.auth.models import User

class BuyerSerializer(serializers.ModelSerializer):
    games = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Buyer
        fields = ['id', 'name', 'balance', 'age', 'registration_date', 'games']

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("Возраст должен быть не менее 18 лет.")
        return value

    def get_games_count(self, obj):
        return obj.games.count()

class GameSerializer(serializers.ModelSerializer):
    buyers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'title', 'cost', 'size', 'description', 'age_limited', 'buyers']

    def validate_cost(self, value):
        if value < 0:
            raise serializers.ValidationError("Стоимость не может быть отрицательной")
        return value

    def validate_size(self, value):
        if value < 0:
            raise serializers.ValidationError("Размер не может быть отрицательным")
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class NewsSerializer(serializers.ModelSerializer):
    short_content = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'short_content', 'date']

    def get_short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherModel
        fields = ['id', 'field1', 'field2']

class ArticleSerializer(serializers.ModelSerializer):
    short_content = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'short_content', 'date']

    def get_short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content