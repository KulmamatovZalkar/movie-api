from rest_framework import serializers

from .models import Movie, Rating, Review, Actor


class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "name", "image")


class ActorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class MovieListSerializer(serializers.ModelSerializer):
    rating_user = serializers.BooleanField()
    """Movies list"""
    class Meta:
        model = Movie
        fields = ("id", "title", "tagline", "category", "rating_user")


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Movies list"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children")


class MovieDetailSerializer(serializers.ModelSerializer):
    """Movie detail"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorDetailSerializer(read_only=True, many=True)
    actors = ActorDetailSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(
        slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft", )


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validate_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validate_data.get('ip', None),
            movie=validate_data.get('movie', None),
            defaults={'star': validate_data.get('star')}
        )

        return rating
