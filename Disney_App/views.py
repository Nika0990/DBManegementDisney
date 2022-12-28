from django.shortcuts import render
from .models import Actorsinmovies, Movies
from django.db import connection

def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def index(request):
    return render(request,'index.html')


def add_movie(request):
    pass


def query_results(request):
    pass
# Create your views here.
