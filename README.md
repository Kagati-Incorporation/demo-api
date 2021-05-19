# Demo API
Backed for E-commerce 

How to run this project
-----------------------

1. <code>docker-compose build</code>
2. <code> docker-compose up -d </code>(Doesn't open interactive window to show errors and warnings. Remove the <code> -d </code> flag to show errors and warnings.)

Makemigrations, Migrate, Createsuperuser
--------------------------
1.<code> docker-compose run web python manage.py makemigrations --app_name-- </code> (To create migrations of the app)

2.<code> docker-compose run web python manage.py migrate --app_name-- </code> (To migrate the changes)

3.<code> docker-compose run web python manage.py createsuperuser </code> (to create superuser)
