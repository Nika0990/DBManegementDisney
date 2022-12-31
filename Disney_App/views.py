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
    with connection.cursor() as cursor:
        cursor.execute("""SELECT Years.genre, yearCount, MaxGrossMovie, MaxGrossMovieGross, MaxLenMovie
            FROM
                       ( SELECT Zero.genre, ISNULL(GenreCount.yearCount,0) as yearCount
                        FROM    (Select genre, 0 as yearCount
                                From Movies
                                Where genre is not null
                                group by genre ) as Zero
                                LEFT OUTER JOIN
                                                (SELECT genre, count(*) as yearCount
                                                    From(   SELECT DISTINCT M1.genre, year(M1.releaseDate) as years
                                                            FROM Movies as M1 LEFT OUTER JOIN Movies as M2
                                                            ON M1.genre = M2.genre
                                                            WHERE M1.genre = M2.genre and year(M1.releaseDate) = year(M2.releaseDate)
                                                                                      and (M1.movieTitle != M2.movieTitle) and M1.genre is not null
                                                            GROUP BY M1.genre, year(M1.releaseDate)) as movieYear
                                                        group by genre) as GenreCount
                        ON Zero.genre = GenreCount.genre) as Years
            FULL OUTER JOIN
                        (SELECT maxGross.genre, movieTitle as MaxGrossMovie, MaxGrossMovieGross
                        FROM (Select genre, MAX(gross) as MaxGrossMovieGross
                                From Movies
                                Where genre is not null
                                GROUP BY genre) as maxGross LEFT OUTER JOIN Movies
                        ON Movies.genre = maxGross.genre
                        WHERE maxGross.MaxGrossMovieGross = Movies.gross) as MovieGross
            ON MovieGross.genre = Years.genre
            FULL OUTER JOIN
                        (SELECT maxLenMovie.genre, min(movieTitle) as MaxLenMovie
                        FROM
                                (SELECT genre, MAX(len(movieTitle)) as maxLen
                                FROM Movies
                                WHERE genre is not null
                                GROUP BY genre) as maxLenMovie
                        FULL OUTER JOIN Movies ON Movies.genre = maxLenMovie.genre
                        WHERE len(Movies.movieTitle) = maxLenMovie.maxLen
                        GROUP BY maxLenMovie.genre) lenMovie
            ON lenMovie.genre = MovieGross.genre""")
        sql_res1 = dictfetchall(cursor)
    return render(request, 'query_results.html', {'sql_res_1': sql_res1})
