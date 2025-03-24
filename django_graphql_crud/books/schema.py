import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from django.db.models import Q
from .models import Book


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = "__all__"


class BookFilterInput(graphene.InputObjectType):
    search = graphene.String()
    author = graphene.String()
    year_min = graphene.Int()
    year_max = graphene.Int()


class Query(graphene.ObjectType):
    all_books = graphene.List(
        BookType,
        filters=BookFilterInput(required=False),
        skip=graphene.Int(required=False),
        limit=graphene.Int(required=False)
    )
    book_by_id = graphene.Field(BookType, id=graphene.Int(required=True))
    my_books = graphene.List(BookType)

    @login_required
    def resolve_all_books(self, info, filters=None, skip=None, limit=None):
        queryset = Book.objects.all()

        if filters:
            if filters.search:
                search_filter = Q(title__icontains=filters.search) | \
                                Q(author__icontains=filters.search) | \
                                Q(description__icontains=filters.search)
                queryset = queryset.filter(search_filter)

            if filters.author:
                queryset = queryset.filter(author__icontains=filters.author)

            if filters.year_min:
                queryset = queryset.filter(year_published__gte=filters.year_min)

            if filters.year_max:
                queryset = queryset.filter(year_published__lte=filters.year_max)

        # Pagination
        if skip:
            queryset = queryset[skip:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    @login_required
    def resolve_book_by_id(self, info, id):
        try:
            return Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return None

    @login_required
    def resolve_my_books(self, info):
        return Book.objects.filter(created_by=info.context.user)


class CreateBookMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        year_published = graphene.Int(required=True)
        isbn = graphene.String(required=True)
        description = graphene.String()

    book = graphene.Field(BookType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, title, author, year_published, isbn, description=""):
        try:
            # Check if book with ISBN already exists
            if Book.objects.filter(isbn=isbn).exists():
                return CreateBookMutation(
                    success=False,
                    message="Book with this ISBN already exists"
                )

            book = Book(
                title=title,
                author=author,
                year_published=year_published,
                isbn=isbn,
                description=description,
                created_by=info.context.user
            )
            book.save()
            return CreateBookMutation(book=book, success=True, message="Book created successfully")
        except Exception as e:
            return CreateBookMutation(success=False, message=str(e))


class UpdateBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        author = graphene.String()
        year_published = graphene.Int()
        isbn = graphene.String()
        description = graphene.String()

    book = graphene.Field(BookType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, id, **kwargs):
        try:
            book = Book.objects.get(pk=id)

            # Check if user has permission (is owner or staff)
            if book.created_by != info.context.user and not info.context.user.is_staff:
                return UpdateBookMutation(
                    success=False,
                    message="You don't have permission to update this book"
                )

            # Check ISBN uniqueness if it's being updated
            if 'isbn' in kwargs and kwargs['isbn'] != book.isbn:
                if Book.objects.filter(isbn=kwargs['isbn']).exists():
                    return UpdateBookMutation(
                        success=False,
                        message="Book with this ISBN already exists"
                    )

            for key, value in kwargs.items():
                if value is not None:
                    setattr(book, key, value)

            book.save()
            return UpdateBookMutation(book=book, success=True, message="Book updated successfully")
        except Book.DoesNotExist:
            return UpdateBookMutation(success=False, message="Book not found")
        except Exception as e:
            return UpdateBookMutation(success=False, message=str(e))


class DeleteBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, id):
        try:
            book = Book.objects.get(pk=id)

            # Check if user has permission (is owner or staff)
            if book.created_by != info.context.user and not info.context.user.is_staff:
                return DeleteBookMutation(
                    success=False,
                    message="You don't have permission to delete this book"
                )

            book.delete()
            return DeleteBookMutation(success=True, message="Book deleted successfully")
        except Book.DoesNotExist:
            return DeleteBookMutation(success=False, message="Book not found")
        except Exception as e:
            return DeleteBookMutation(success=False, message=str(e))


class Mutation(graphene.ObjectType):
    create_book = CreateBookMutation.Field()
    update_book = UpdateBookMutation.Field()
    delete_book = DeleteBookMutation.Field()