import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
import graphql_jwt
from graphql_jwt.decorators import login_required

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, username, password, email, first_name="", last_name=""):
        try:
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return CreateUserMutation(success=False, message="Username already exists")

            if User.objects.filter(email=email).exists():
                return CreateUserMutation(success=False, message="Email already exists")

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            return CreateUserMutation(user=user, success=True, message="User created successfully")
        except Exception as e:
            return CreateUserMutation(success=False, message=str(e))


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, id, **kwargs):
        try:
            user = User.objects.get(pk=id)

            # Only allow users to update their own profile unless they're staff
            if str(user.id) != id and not info.context.user.is_staff:
                return UpdateUserMutation(success=False, message="You don't have permission to update this user")

            for key, value in kwargs.items():
                if value is not None:
                    setattr(user, key, value)

            user.save()
            return UpdateUserMutation(user=user, success=True, message="User updated successfully")
        except User.DoesNotExist:
            return UpdateUserMutation(success=False, message="User not found")
        except Exception as e:
            return UpdateUserMutation(success=False, message=str(e))


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))

    @login_required
    def resolve_me(self, info):
        return info.context.user

    @login_required
    def resolve_users(self, info):
        # Only staff can view all users
        if info.context.user.is_staff:
            return User.objects.all()
        return []

    @login_required
    def resolve_user(self, info, id):
        # Staff can view any user, regular users can only view themselves
        if info.context.user.is_staff or str(info.context.user.id) == id:
            try:
                return User.objects.get(pk=id)
            except User.DoesNotExist:
                return None
        return None


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()

    # JWT Authentication mutations
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()