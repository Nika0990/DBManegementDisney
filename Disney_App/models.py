# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actorsinmovies(models.Model):
    movie = models.OneToOneField('Movies', models.DO_NOTHING, db_column='movie', primary_key=True)
    actor = models.CharField(max_length=50)
    actorrole = models.CharField(db_column='actorRole', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ActorsInMovies'
        unique_together = (('movie', 'actor', 'actorrole'),)


class Movies(models.Model):
    movietitle = models.CharField(db_column='movieTitle', primary_key=True, max_length=50)  # Field name made lowercase.
    releasedate = models.DateField(db_column='releaseDate', blank=True, null=True)  # Field name made lowercase.
    genre = models.CharField(max_length=20, blank=True, null=True)
    rating = models.CharField(max_length=20, blank=True, null=True)
    gross = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Movies'
