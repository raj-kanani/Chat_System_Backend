### Clone git project repository to your local system: 

    git clone https://github.com/raj-kanani/Chat_System_Backend

### Create virtual environment

```
$ virtualenv venv
```

### Activate virtual environment

```
$ source venv/bin/activate
```

### Login into 2factor.in to get SMS_API_KEY :

 https://2factor.in/


### Migration command

```
$ python manage.py makemigrations
$ python manage.py migrate

Performing migrations the perform migrations on each service individually.
The order is mentioned below:
	>>> my_app
```

### Create super admin user

```
$  python manage.py createsuperuser
	>>>  email_address : demo@gmail.com
	>>>  username : demo123
	>>>  password : demo@123
```

### Run django server

```
$ python3 manage.py runserver
```

### Start celery worker

    celery -A my_app worker --loglevel=info

### start celery beat

    celery -A my_app beat --loglevel=info



### You can now access the file api service on your browser by using

    http://localhost:8000/api/

### Docker commands :

### Build and Start Containers
    docker-compose up --build

### Migrate the Database
    docker-compose exec web python manage.py migrate

### Create a superuser
    docker-compose exec web python manage.py createsuperuser


