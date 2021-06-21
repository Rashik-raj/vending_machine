# vending_machine
A short app immitating vending machine

# how to run
1. Clone the project and change the dir to the project.
2. Create virtual env by `python -m venv env` next to **manage.py** file.
3. Activate virtual env by `source env/bin/activate`.
4. Install requirements from requirements.txt file by `pip install -r requirements.txt`.
5. Create migration files `python manage.py makemigrations`.
6. Migrate database `python manage.py migrate`.
7. Apply fixture by `python manage.py loaddata data`.
8. Run the server by `python manage.py runserver`.
