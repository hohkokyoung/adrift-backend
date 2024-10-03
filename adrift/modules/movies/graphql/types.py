import graphene
from core.api.graphql.types import RelayObjectType
from movies.models import (
    Movie, Genre, Person, 
    MoviePerson, MoviePersonAward, Award, 
    AwardCategory, Company, Language, 
    Review, Tagline,
)

class GenreNode(RelayObjectType):
    class Meta:
        model = Genre
        filter_fields = ["name"]
        fields = "__all__"

class MovieNode(RelayObjectType):
    class Meta:
        model = Movie
        filter_fields = ["title"]
        fields = "__all__"

class PersonNode(RelayObjectType):
    class Meta:
        model = Person
        filter_fields = ["name"]
        fields = "__all__"

class MoviePersonNode(RelayObjectType):
    class Meta:
        model = MoviePerson
        filter_fields = ["movie"]
        fields = "__all__"

class MoviePersonAwardNode(RelayObjectType):
    class Meta:
        model = MoviePersonAward
        filter_fields = ["movie_person"]
        fields = "__all__"

class AwardNode(RelayObjectType):
    class Meta:
        model = Award
        filter_fields = ["name"]
        fields = "__all__"

class AwardCategoryNode(RelayObjectType):
    class Meta:
        model = AwardCategory
        filter_fields = ["award"]
        fields = "__all__"

class CompanyNode(RelayObjectType):
    class Meta:
        model = Company
        filter_fields = ["name"]
        fields = "__all__"

class LanguageNode(RelayObjectType):
    class Meta:
        model = Language
        filter_fields = ["name"]
        fields = "__all__"

class ReviewNode(RelayObjectType):
    class Meta:
        model = Review
        filter_fields = ["comment"]
        fields = "__all__"

class TaglineNode(RelayObjectType):
    class Meta:
        model = Tagline
        filter_fields = ["description"]
        fields = "__all__"
