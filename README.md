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

Alle kommandoer og filer er kun veiledene.

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

Opprett mapper til apache-ting (legg dem gjerne til i .gitignore):

```
mkdir /srv/dokuspokus/apache/static/
mkdir /srv/dokuspokus/apache/logs/
mkdir /srv/dokuspokus/apache/conf/
mkdir /srv/dokuspokus/run/eggs/
```

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
~$ service apache2 restart
```

Wikien burde nå være oppe og gå på wiki.radiorevolt.no

## TODO

### Ajax-bildeopplasting
Støtte for å kunne laste opp bilder, og kunne finne eksisterende bilder fra databasen. F.eks. en knapp som åpnet et nytt (lite) vindu der du kan søke et eksisterende bilder og laste opp nye bilder. Bildene burde lagres i en tabell i databasen, og hvert bilde burde ha en tittel og bildetekst.

### Brukerside
Hver bruker får en side der man kan se navnet, telefonnummeret og epostadressen til personen. URL-en kan f.eks. være på formen /view/bruker:<brukernavn>.html eller /user/<brukernavn>.html. Det første alternativet er enklest, da linker til brukerprofiler blir veldig enkelt implementert i wikien ved kun å skrive `[[bruker:<brukernavn>]]`. Det andre alternavtivet er mest logisk, og ser penest ut. Det krever i midlertidig at vi lager en måte å linke til brukere på i wikien. Dette er uansett enkelt å endre på senere.

### Egendefinerte titteler på sider
Vi brude kvitte oss med den nåværende løsningen med wikilinker, da den ikke er spesielt god. Den støtter kun sider med tittler på python sitt tittelformat ("dettE er Min sIDE" -> "Dette Er Min Side", "DigAIRange" -> "Digairange", "RESTful API" -> "Restful Api", "iPhone" -> "Iphone"). Dette er litt dumt da man burde kunne velge om man vil ha små eller store bokstaver. Den opprinnlige ideen bak dette var å hindre folk å lage stygge tittler, men jeg tror det er en større hindring enn det er en gevinst.

Dette kan løses ved f.eks. å lage et tittelfelt i _create.html_, som automatisk poppuleres med slik tittelene blir generert i dag ("/view/min_nye_side.html" -> "Min Nye Side"). Da vil de fleste benytte denne formen på tittelen, mens man i spesialtilfeller kan endre den.

Samtidig må man passe på å beholde linkingen slik at det ikke spiller noen rolle om man skriver små eller store bokstaver i linkingen. Dvs: Vi må passe på at `[[Dette er min side]]`, `[[dette er min side]]`, `[[Dette Er Min Side]]` alle linker til samme side. Måten dette er løst på nå er at view-funksjonen ufører `.lower()` på url-en. Dette er en ok løsning som fremdeles burde være tilstrekkelig etter vi har implemetert egendefinerte tittler.

### Egendefinerte funksjoner
Vi burde ha muligheten for å legge til egenlagde markdownfunksjoner. Den enkleste måten å legge til det på er å benytte [django_markdown_shortcodes](https://github.com/defbyte/django-markdown-shortcodes). Da tror jeg du kunne være lurt å fjerne wikilinks-utvidelsen vi har i markdown nå, og heller lage en shortcode for det, f.eks.: `[[side "<navn på siden>" "<visningsnavnet til linken>"]]` der det siste parameteret er valgfritt. Det kan kankskje også være aktuelt å kunne spesifisere en id fra en header, slik at man kan linke direkte til et segment av siden (linkene man finner i innholdsfortegnelser). Dette kan f.eks. bare være: ``[[side "<navn på siden>" "<visningsnavnet til linken>" "<navn på segment>"]]` (for å linke til et segment på siden burde visningsnavn være påkrevd). Eventuelt kan det lages slik: `[[side "<navn på siden>#<navn på segment>" "<visningsnavnet til linken>"]]`. Det ødelegger for å ha linker med "#" i seg, men det er kanskje ikke så farlig. I tillegg så slipper man å kreve visningsnavn når man linker til segmentet (default visningsnavn kan bare være <navn på siden>#<navn på segment>).

En annen funksjon vi da kan lage er `[[bruker "<brukernavn>" "<visningsnavn til linken>"]]`, der siste parameter er valgfri (default kan f.eks. være navnet til brukeren).

Andre funksjoner:
* En funksjon som henter lydklipp fra en mappe i digas (ala podcast-mappen) og embedder dem.
* En funksjon som embedder youtube, vimeo o.l. (responsivt)
* En funksjon som går gjennom alle linker og markerer dem om de gir 404
