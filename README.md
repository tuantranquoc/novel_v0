## Novels crawler app allow craw novels on certain website

1. <https://metruyenchu.com>
2. <https://nuhiep.com>
3. <https://vtruyen.com>
4. <https://wikidich.com>
5. <https://bachngocsach.com>
6. <https://truyen.tangthuvien.vn>

## Technologies used

1. Django version 3.0.7
2. postgres (PostgreSQL) 12.3
3. Python 3.8.3rc1

## How to install

> pip install -r requirements.txt

## Next step

> download and install ChromeDriver 87.0.4280.20 (link download: <https://chromedriver.chromium.org/downloads>)

## Setting up database

0. Database: postgresql (Link download: <https://www.postgresql.org/download/>)
1. Database name use for project: "novel"
2. User: "postgres"
3. Password: "password"
4. Host: "localhost"
5. Port: "5432"

> DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'novel',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

## Start project

### Create admin account

> py ./manage.py createsuperuser

### Start app

> py ./manage.py crawler

### Select 0 to provide "path to chromedriver.exe"

> example: 'C:\Program Files (x86)\chromedriver.exe'

### Run app again and select option 1 - 6 to craw novels from provided website
### Note: <https://wikidich.com> use DOS detection  

### Run server and test data

> py ./manage.py runserver
