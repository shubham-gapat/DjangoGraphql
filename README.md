# Django GraphQL Project

A beginner-friendly implementation of GraphQL in Django using Graphene-Django.

## Overview

This project demonstrates how to integrate GraphQL with Django, providing a flexible API with a single endpoint. It includes examples of queries and mutations for a basic book management system.

## Features

- Single GraphQL endpoint
- Query operations to retrieve data
- Mutation operations to modify data
- Filtering capabilities
- Basic authentication integration
- GraphiQL interface for API testing

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/django-graphql-project.git
   cd django-graphql-project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install django graphene-django
   ```

4. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Visit `http://localhost:8000/graphql/` to access the GraphiQL interface.

## Project Structure

```
graphql_project/
├── api/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── schema.py
│   ├── tests.py
│   └── views.py
├── graphql_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── schema.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── README.md
```

## Usage

### GraphQL Queries

Access all books:
```graphql
query {
  allBooks {
    id
    title
    author
    yearPublished
    isPublished
  }
}
```

Filter books by year:
```graphql
query {
  allBooks(year: 2020) {
    id
    title
    author
    yearPublished
  }
}
```

Get book by ID:
```graphql
query {
  bookById(id: 1) {
    title
    author
    yearPublished
  }
}
```

### GraphQL Mutations

Create a new book:
```graphql
mutation {
  createBook(
    title: "Django for Professionals"
    author: "William S. Vincent"
    yearPublished: 2022
    isPublished: true
  ) {
    book {
      id
      title
      author
      yearPublished
      isPublished
    }
  }
}
```

## Authentication

The project includes basic authentication for GraphQL operations. To access protected queries and mutations:

1. Create a user through Django admin or the `createsuperuser` command
2. Log in through Django's authentication system
3. Access the GraphQL endpoint with your authenticated session

## Extending the Project

### Adding New Models

1. Define your model in `api/models.py`
2. Create types and queries in `api/schema.py`
3. Include your schema in the project's root schema
4. Apply migrations

### Adding Additional Mutations

1. Define a new mutation class in `api/schema.py`
2. Add the mutation to the Mutation class
3. Update the schema to include your new mutation

## Troubleshooting

- **Migrations issues**: Make sure your app is in `INSTALLED_APPS` in settings.py
- **GraphQL errors**: Check your schema definition for syntax errors
- **Authentication problems**: Ensure you're logged in if using protected endpoints

## Best Practices

- Structure your schema logically by app
- Use input types for complex mutations
- Implement proper authentication and authorization
- Consider batching database queries to avoid the N+1 query problem
- Use pagination for large datasets
- Write tests for your GraphQL schema

## Resources

- [Graphene-Django Documentation](https://docs.graphene-python.org/projects/django/en/latest/)
- [Django Documentation](https://docs.djangoproject.com/)
- [GraphQL Official Website](https://graphql.org/)

