# Project 2: Commerce

[Background, Getting Started, Specification, Hints](https://cs50.harvard.edu/web/2020/projects/2/commerce/)

## Useful commands

### Running the project
````bash 
python manage.py runserver
````

## Getting Started

### Setup python instance (first time only)

1. Create a virutal env for running python: 
    ````bash 
    python3 -m venv myenv
    ````
2. Activate the env: 
    ````bash
    source myenv/bin/activate
    ````
3. Install Django: 
    ````bash
    pip install Django
    ````

### Apply migrations

1. Download the distribution code from https://cdn.cs50.net/web/2020/spring/projects/2/commerce.zip and unzip it.
2. In your terminal, cd into the commerce directory.
3. Run `python manage.py makemigrations` auctions to make migrations for the `auctions` app.
4. Run `python manage.py migrate` to apply migrations to your database.