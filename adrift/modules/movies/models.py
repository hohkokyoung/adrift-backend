from django.db import models
from core.models import BaseModel, Address
from core.enums import Gender as GenderEnum
from .enums import MPAA as MPAAEnum, Role as RoleEnum, Company as CompanyEnum
from django_countries.fields import CountryField
from languages.fields import LanguageField

class Genre(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        indexes = [models.Index(fields=['name'])]

class MovieGenre(BaseModel):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    class Meta:
        app_label = "movies"

class Person(BaseModel):
    name = models.CharField(max_length=255)
    birth_name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=30,
        choices=[(enum.name, enum.value) for enum in GenderEnum]
    )
    date_of_birth = models.DateTimeField()
    place_of_birth = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="persons")
    biography = models.TextField()

    class Meta:
        ordering = ["name"]

class Award(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    organization = models.CharField(max_length=255)
    year = models.IntegerField()
    country = CountryField()

    class Meta:
        ordering = ["name"]

class AwardCategory(BaseModel):
    award = models.ForeignKey(Award, on_delete=models.CASCADE, related_name="award_categories")

class MovieAward(BaseModel):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    award = models.ForeignKey('Award', on_delete=models.CASCADE)
    year = models.IntegerField()
    won = models.BooleanField(default=False)

    class Meta:
        app_label = "movies"

class Company(BaseModel):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=30,
        choices=[(enum.name, enum.value) for enum in CompanyEnum]
    )

    class Meta:
        ordering = ["name"]

class MovieCompany(BaseModel):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)

    class Meta:
        app_label = "movies"

class Movie(BaseModel):
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    synopsis = models.TextField()
    poster_url = models.URLField()
    trailer_url = models.URLField()
    mpaa_rating = models.CharField(
        max_length=10,
        choices=[(enum.name, enum.value) for enum in MPAAEnum]
    )
    budget = models.IntegerField()
    box_office = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name="movies", through=MovieGenre, through_fields=("movie", "genre"))
    awards = models.ManyToManyField(Award, related_name="movies", through=MovieAward, through_fields=("movie", "award"))
    companies = models.ManyToManyField(Company, related_name="movies", through=MovieCompany, through_fields=("movie", "company"))

    class Meta:
        indexes = [models.Index(fields=['title'])]


class Language(BaseModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="languages")
    name = LanguageField()

    class Meta:
        ordering = ["movie"]

class Review(BaseModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    comment = models.TextField()

    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]

    rating = models.IntegerField(choices=RATING_CHOICES, default=1)

    class Meta:
        ordering = ["rating"]

class Tagline(BaseModel):
    description = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="taglines")

    class Meta:
        ordering = ["description"]

class MoviePerson(BaseModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_persons")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="movie_persons")
    type = models.CharField(
        max_length=30,
        choices=[(enum.name, enum.value) for enum in RoleEnum]
    )
    character = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["movie"]

# one person in a movie role (director/writer/musician/actor/actress) can have multiple awards and vice versa
class MoviePersonAward(BaseModel):
    movie_person = models.ForeignKey(MoviePerson, on_delete=models.CASCADE, related_name="movie_person_awards")
    award = models.ForeignKey(Award, on_delete=models.CASCADE, related_name="movie_person_awards")

    class Meta:
        ordering = ["movie_person"]


