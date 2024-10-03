import graphene

import users.graphql.schema as user_schema
import movies.graphql.schema as movie_schema
import bookings.graphql.schema as booking_schema
import theaters.graphql.schema as theater_schema

class Query(
    user_schema.Query,
    movie_schema.Query,
    booking_schema.Query,
    theater_schema.Query,
):
    pass

class Mutation(
    user_schema.Mutation,
    # movie_schema.Mutation
    # booking_schema.Mutation,
    theater_schema.Mutation
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)