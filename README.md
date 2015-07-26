# Dokuspokus Wiki
En intern wiki for Radio Revolt.

## Installasjon
Sett opp et virituelt miljø:

```
~$ virtualenv -p <filbane-til-python-3> venv
~$ source venv/bin/activate
```

`python --version` burde gi 3.4.0 eller nyere.


Installer avhengigheter:

```
~$ pip install -r requirements.txt
```

Bygg databasen:

```
~$ python manage.py migrate
```

Bygg søkeindekser:

```
~$ python manage.py rebuild_index
```

Lag superbruker:

```
~$ python manage.py createsuperuser
```

Det burde nå fungere å kjøre den med `python manage.py runserver`.

## Deploy
Vil helst ikke deploye med `python manage.py runserver`. Bedre å bruke apache til
å serve.

Her brukers Apache med mod_wsgi for å deploye. Andre alternativer finnes, men dette er den enkleste.

Installer mod_wsgi:

```
~$ apt-get install libapache2-mod-wsgi
```

Flytt dokuspokus til et fornuftig sted på serveren, f.eks. /srv/dokuspokus

Endre følgende i page/settings.py:

```python
...

DEBUG = False

ALLOWED_HOSTS = ['*']

...

STATIC_ROOT = '/srv/dokuspokus/apache/static/'
```

Opprett følgende mapper (legg dem gjerne til i .gitignore):

* `/srv/dokuspokus/apache/static/`
* `/srv/dokuspokus/apache/logs/`
* `/srv/dokuspokus/apache/conf/`
* `/srv/dokuspokus/run/eggs/`

Opprett to log-filer:

```
~$ touch /srv/dokuspokus/apache/logs/error.log
~$ touch /srv/dokuspokus/apache/logs/access.log
```

Lag WSGI-configurasjonsfilen '/srv/dokuspokus/apache/conf/wsgi.py':

```
import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, root_path)
sys.path.insert(0, os.path.abspath(os.path.join(root_path, 'venv/lib/python3.4/site-packages/')))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "page.settings")

application = get_wsgi_application()
```

Eksporter statiske filer:

```
~$ python manage.py collectstatic
```

Lag en dokuspokus-bruker og -gruppe:

```
~$ adduser --no-create-home dokuspokus
~$ addgroup dokuspokus
~$ usermod -aG dokuspokus dokuspokus
```

Endre rettighetene til dokuspokus-mappen:

```
~$ chown -R dokuspokus:dokuspokus /srv/dokuspokus/
~$ chmod -R 755 /srv/dokuspokus/
~$ chmod -R 777 /srv/dokuspokus/apache/conf/
```

Lag en virtual host til wikien:

```
<VirtualHost *:80>
        ServerAdmin radioteknisk@studentmediene.no
        ServerName wiki.radiorevolt.no
        ServerAlias www.wiki.radiorevolt.no

        CustomLog /srv/dokuspokus/apache/logs/access.log combined
        ErrorLog /srv/dokuspokus/apache/logs/error.log
        LogLevel warn

        Alias /static/ /srv/dokuspokus/apache/static/

        <Directory /srv/dokuspokus/apache/static/>
                Require all granted
        </Directory>

        WSGIDaemonProcess wiki.radiorevolt.no user=homepage group=homepage processes=1 threads=15 maximum-requests=10000 python-path=/srv/dokuspokus/venv/lib/python3.4/site-packages python-eggs=/srv/dokuspokus/run/eggs
        WSGIProcessGroup wiki.radiorevolt.no
        WSGIScriptAlias / /srv/dokuspokus/apache/conf/wsgi.py

        <Directory /srv/dokuspokus/apache/conf/>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>

</VirtualHost>
```