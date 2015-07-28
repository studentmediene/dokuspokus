# Dokuspokus Wiki
En intern wiki for Radio Revolt.

## Bidra
Dersom du ønsker å bidra må du først sette opp systemet lokalt, se [Oppsett](https://github.com/RadioRevolt/dokuspokus#oppsett).

**All kode og kommentarer i koden, samt commit-meldinger, skal være på engelsk.**

1. Gå til [issues](https://github.com/RadioRevolt/dokuspokus/issues) og finn en du har lyst til å jobbe på.
2. Velg helst enn fra en [milestone](https://github.com/RadioRevolt/dokuspokus/milestones) med forfall om ikke så veldig lenge.
2. Kommenter i issuet at du jobber på det.
3. Pass på at du er på develop-branchen lokalt.
4. Lag en egen branch med navn: "issue - \<navn på issue\> (#\<issue ID\>)".
5. Bytt til branchen du nettopp lagde og push den til github (slik at andre kan se at du jobber på den).
6. Når du har fikset issuet, commit endringene med følgende medling: "\<hva du har gjort\>. Fixes #\<issue ID\>"
7. Lag en [pull request](https://github.com/RadioRevolt/dokuspokus/pulls) med branchen din, og develop-branchen som base.

## Installasjon
Her er en detaljert beskrivelse på hvordan du kan kjøre systemet lokalt.

### Avhengigheter
Før du begynner må du ha disse verktøyene:
* __[Python 3]__ - Programmeringsspråket wikien er skrevet i.
* __[Django]__ - Rammeverket som er brukt i wikien.
* __[pip]__ - Et pakkeinstallasjonsprogram for Python.
* __[git]__ - Et versjonshåndteringsprogram.
* __[virtualenv]__ - Et program for å generere et uviklingsmiljø wikien kan kjøre i.

[Python 3]: https://www.python.org/
[Django]: https://www.djangoproject.com/
[pip]: https://pip.pypa.io/
[git]: https://git-scm.com/
[virtualenv]: https://virtualenv.pypa.io/

###Oppsett
Hent kildekoden:
```
$ git clone git@github.com:RadioRevolt/dokuspokus.git
```

Sett opp et virituelt miljø:

```
$ virtualenv -p <filbane-til-python-3> venv
$ source venv/bin/activate
```

`python --version` burde gi 3.4.0 eller nyere.


Installer avhengigheter:

```
$ pip install -r requirements.txt
```

Bygg databasen:

```
$ python manage.py migrate
```

Bygg søkeindekser:

```
$ python manage.py rebuild_index
```

Lag superbruker:

```
$ python manage.py createsuperuser
```

Det burde nå fungere å kjøre den med `python manage.py runserver`. Du vil da kunne besøke wikien i nettleseren din på `http://localhost:8000`

## Deploy
Vil helst ikke deploye med `python manage.py runserver`. Bedre å bruke apache til
å serve.
Her brukers Apache med mod_wsgi for å deploye. Andre alternativer finnes, men dette er den enkleste.

Alle kommandoer og filer er kun veiledene.

Installer mod_wsgi:

```
$ apt-get install libapache2-mod-wsgi
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

Opprett mapper til apache-ting (legg dem gjerne til i .gitignore):

```
mkdir /srv/dokuspokus/apache/static/
mkdir /srv/dokuspokus/apache/logs/
mkdir /srv/dokuspokus/apache/conf/
mkdir /srv/dokuspokus/run/eggs/
```

Opprett to log-filer:

```
$ touch /srv/dokuspokus/apache/logs/error.log
$ touch /srv/dokuspokus/apache/logs/access.log
```

Lag WSGI-configurasjonsfilen '/srv/dokuspokus/apache/conf/wsgi.py':

```python
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
$ python manage.py collectstatic
```

Lag en dokuspokus-bruker og -gruppe:

```
$ adduser --no-create-home dokuspokus
$ addgroup dokuspokus
$ usermod -aG dokuspokus dokuspokus
```

Endre rettighetene til dokuspokus-mappen:

```
$ chown -R dokuspokus:dokuspokus /srv/dokuspokus/
$ chmod -R 755 /srv/dokuspokus/
$ chmod -R 777 /srv/dokuspokus/apache/conf/
```

Lag en virtual host til wikien:

```apache
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

    WSGIDaemonProcess wiki.radiorevolt.no user=dokuspokus group=dokuspokus processes=1 threads=15 maximum-requests=10000 python-path=/srv/dokuspokus/venv/lib/python3.4/site-packages python-eggs=/srv/dokuspokus/run/eggs
    WSGIProcessGroup wiki.radiorevolt.no
    WSGIScriptAlias / /srv/dokuspokus/apache/conf/wsgi.py
    
    <Directory /srv/dokuspokus/apache/conf/>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

</VirtualHost>
```

Restart apache:

```
$ service apache2 restart
```

Wikien burde nå være oppe og gå på wiki.radiorevolt.no
