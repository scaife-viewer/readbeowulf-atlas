# Readbeowulf Atlas

ATLAS Server for Readbeowulf.

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv`
or `pyenv`).

```
pip install -r requirements-dev.txt
```

Create a PostgreSQL database `readbeowulf_atlas`:

```
createdb readbeowulf_atlas
```

Populate the database:

```
./manage.py migrate
./manage.py loaddata sites
```

Run the Django dev server:
```
./manage.py runserver
```

Browse to http://localhost:8000/

## Loading data

Create a superuser:

```
./manage.py createsuperuser
```

Run the `import_versions` script:

```
./manage.py shell -c 'from readbeowulf_atlas.library.importers import import_versions; import_versions();'
```

## Sample Queries

Access the interactive GraphQL explorer at `http://localhost:8000/graphql/`.

Retrieve all the fitts.
```
{
  fitts {
    edges {
      node {
        id
        label
        position
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

Retrieve the first ten half-lines.
```
{
  halflines(first: 10) {
    edges {
      node {
        id
        label
        position
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```


Retrieve only the second part of the final ten half-lines.
```
{
  halflines(last: 10, position: "b") {
    edges {
      node {
        id
        label
        position
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

Get the first token of every paragraph along with its gloss.
```
{
  tokens(firstInParagraph: true) {
    edges {
      node {
        id
        textContent
        gloss
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```
