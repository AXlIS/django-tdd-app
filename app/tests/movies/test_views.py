import json
import pytest
from rest_framework import status
from django.urls import reverse

from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    response = client.post(
        reverse('add_movie'),
        {
            "title": "The Big Lebowski",
            "genre": "comedy",
            "year": "1998",
        }
    )

    movie = Movie.objects.all()[0]

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == movie.title


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {},
        content_type="application/json"
    )
    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_add_movie_invalid_json_keys(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {
            "title": "The Big Lebowski",
            "genre": "comedy",
        },
        content_type="application/json"
    )
    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    movie = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    response = client.get(reverse("get_movie", args=[movie.id]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == movie.id


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    first_movie = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    second_movie = add_movie("No Country for Old Men", "thriller", "2007")
    response = client.get(reverse('add_movie'))
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['title'] == first_movie.title
    assert response.data[1]['title'] == second_movie.title
