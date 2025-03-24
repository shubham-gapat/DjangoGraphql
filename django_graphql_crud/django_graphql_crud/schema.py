import graphene
import books.schema
import users.schema

class Query(books.schema.Query, users.schema.Query, graphene.ObjectType):
    pass

class Mutation(books.schema.Mutation, users.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)