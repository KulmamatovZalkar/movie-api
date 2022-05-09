from django.db import models
from rest_framework import generics, permissions

from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie, Actor
from .serializers import CreateRatingSerializer, MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, ActorListSerializer, ActorDetailSerializer
from .service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    """List moviews"""

    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Case(
                models.When(rating__ip=get_client_ip(self.request), then=True),
                default=False,
                output_field=models.BooleanField()
            )
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """List moviews"""
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.filter(draft=False)


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer


class AddStarRatingViews(generics.CreateAPIView):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
