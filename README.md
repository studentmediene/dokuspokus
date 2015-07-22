# dokuspokus
Dokumentasjon for Radio Revolt

## Oppsett av Sublime
Det anbefales å bruke Sublime til å skrive dokumentasjon.
Du kan installere Sublime Text 3 [her](http://www.sublimetext.com/3).

### Utvideleser
Før du kan installere utvideleser må du installere *Package Control*. Det gjør du ved å gå til `view -> show console`, lim inn følgende og trykk på enter:

```
import urllib.request,os,hashlib; h = 'eb2297e1a458f27d836c04bb0cbaf282' + 'd0e7a3098092775ccb37ca9d6b2e4b7d'; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); by = urllib.request.urlopen( 'http://packagecontrol.io/' + pf.replace(' ', '%20')).read(); dh = hashlib.sha256(by).hexdigest(); print('Error validating download (got %s instead of %s), please try manual install' % (dh, h)) if dh != h else open(os.path.join( ipp, pf), 'wb' ).write(by)
```

Deretter kan du installere pakker ved å trykke `ctrl+shift+p` og skrive *install package* og trykke enter på den som heter "Package Control: Install Package". Da åpnes et nytt søkefelt der du kan søke etter og installere utvidelser.

Installer følgende utvidelser(følg instruksjonene på packagecontrol.io-sidene):

* [Markdown Preview](https://packagecontrol.io/packages/Markdown%20Preview)
* [Markdown​Editing](https://packagecontrol.io/packages/MarkdownEditing)
* [Afterglow](https://packagecontrol.io/packages/Theme%20-%20Afterglow)

Gå til `Preferences -> Settings - User` og erstatt alt der med følgende følgende:

```
{
	"caret_extra_width": 1,
	"theme": "Afterglow.sublime-theme",
	"color_scheme": "Packages/Theme - Afterglow/Afterglow.tmTheme",
	"tabs_medium": true,
	"font_options":
	[
		"no_round"
	],
	"font_size": 12,
	"highlight_line": true,
	"ignored_packages":
	[
		"Vintage"
	],
	"word_wrap": true
}
```

Restart Sublime.


## Installer Git
Installer Git (Git Bash om du er på windows).

### Windows
Installer [Git Bash](https://git-scm.com/downloads).

## Sett opp Git

* Åpne git (git bash om du er på windows). Naviger til hjemmemappen din: `cd ~`.
* Klon denne repositoryen: `git clone https://github.com/RadioRevolt/dokuspokus.git`
* Naviger til repositoryen du nettopp klona `cd dokuspokus`

## Bruke Git

* Ny branch: `git checkout -b "<navn-på-branch>"`
* Commite filer til branchen din: `git commit -a -m "<hvilke endringer har du gjort?>"`
* Dytte endringene (commitsene) dine til github: `git push origin <navnet-på-branchen-din>`

## Å skrive dokumentasjon
Dokumentasjonen skrives med markdownsyntaks. Referanse kan du finne [her](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

### Nytt dokument(asjon)
Lag en ny branch som heter navnet på det nye dokumentet du skriver. Når du er ferdig, lag en pullrequest med master. Slett branchen når det er blitt merget.

### Fikse eksisterende dokument(asjon)
Lag en ny branch med følgende navnekonvensjon: "<navnet på dokumentet du skal endre>-edit". Når du er ferdig, lag en pullrequest med master. Slett branchen når det er blitt merget.
