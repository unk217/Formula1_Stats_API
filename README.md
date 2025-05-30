
# F1 Stast API

API con informacion scrapeada de la web de la F1



## Installation

create virtualenv

```bash
  python -m venv venv
```
```bash
  ./venv/Scripts/activate
```
 install requirements   
 ```bash
  pip install -r requirements.txt
```
migrations
 ```bash
  python manage.py makemigrations
```
 ```bash
  python manage.py migrate
```
run scraper
 ```bash
  python manage.py driver_scraper
```
```bash
  python manage.py event_scraper
```
run server
```bash
  python manage.py runserver
```
