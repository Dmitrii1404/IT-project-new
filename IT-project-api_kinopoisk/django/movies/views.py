from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie, Category, Actor, Genre, Rating, Reviews
from .forms import ReviewForm, RatingForm


class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, ListView):
    """Список фильмов"""

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 3


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации о актере"""

    model = Actor
    template_name = "movies/actor.html"
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""

    paginate_by = 2

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year"))
            | Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = "".join(
            [f"year={x}&" for x in self.request.GET.getlist("year")]
        )
        context["genre"] = "".join(
            [f"genre={x}&" for x in self.request.GET.getlist("genre")]
        )
        return context


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""

    def get_queryset(self):
        queryset = (
            Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year"))
                | Q(genres__in=self.request.GET.getlist("genre"))
            )
            .distinct()
            .values("title", "tagline", "url", "poster")
        )
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={"star_id": int(request.POST.get("star"))},
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


from django.shortcuts import render
from django.views import View
import requests
import json


class APISearch(View):


    headers = {
        "accept": "application/json",
        "X-API-KEY": "5J5BGMF-KN14VC9-HW608YR-W4A3P7X"
    }

    def search_by_name(self, name_, page=1, limit=10):
        url = f"https://api.kinopoisk.dev/v1.4/movie/search?page={page}&limit={limit}&query={name_}"
        response = requests.get(url, headers=self.headers)
        return json.loads(response.text)

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            page = 1

        if query:
            data = self.search_by_name(query, page=page)
            movies = data.get("docs", [])
            page_info = data.get("page", {})
            has_next = page_info.get("hasNext", False) if isinstance(page_info, dict) else False

            context = {
                "movies": movies,
                "query": query,
                "page": page,
                "has_next": has_next
            }
            return render(request, "movies/api_search.html", context)
        return render(request, "movies/api_search.html")


import requests
import json

class MovieDetail(View):
    headers = {
        "accept": "application/json",
        "X-API-KEY": "5J5BGMF-KN14VC9-HW608YR-W4A3P7X"
    }

    def get_movie_details(self, movie_id):
        url = f"https://api.kinopoisk.dev/v1.3/movie/{movie_id}"
        response = requests.get(url, headers=self.headers)
        return json.loads(response.text)

    def get(self, request, movie_id, *args, **kwargs):
        movie = self.get_movie_details(movie_id)
        context = {
            "movie": movie
        }
        return render(request, "movies/movie_detail2.html", context)