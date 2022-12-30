from django.shortcuts import render
from .models import Actorsinmovies, Movies
from django.db import connection


def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def index(request):
    return render(request, 'index.html')


def add_movie(request):
    if request.method == 'POST' and request.POST:
        movie_title = request.POST["MovieTitle"]
        release_date = request.POST["release"]
        genre = request.POST["Genre"]
        new_rating = request.POST["Rating"]
        new_gross = request.POST["Gross"]
        new_Movie = Movies(movietitle=movie_title, releasedate=release_date,
                           genre=genre, rating=new_rating, gross=new_gross)
        new_Movie.save()
    return render(request, 'add_movie.html')


def query_results(request):
    sql1 = """
                SELECT genre, count(*) as yearCount
                From(   SELECT DISTINCT M1.genre, year(M1.releaseDate) as years
                FROM Movies as M1, Movies as M2
                WHERE M1.genre = M2.genre and year(M1.releaseDate) = year(M2.releaseDate) and (M1.movieTitle != M2.movieTitle)
                GROUP BY M1.genre, year(M1.releaseDate)) as movieYear
                group by genre"""
    sql_res1 = Movies.objects.raw(sql1)
    return render(request, 'query_results.html', {'sql_res_1': sql_res1})
