# folder-watch

## Zusammenfassung
Dieses Programm überprüft ob sich die Dateien in einem Verzeichnis ändern. 

## Parameter werden in der Datei app.py gesetzt:
SERVER = SQL Server host Name
DATABASE = eine beliebige Datenbank auf dem server
INTERVAL = Intervall in dem gescannt wird
PATH = UNC Pfad zum Verzeichnis, \\-Zeichen müssen escaped werden
VERTEILER Liste von sms-mail Adressen: Mobile-Nr1@sms.bs.ch;Mobile-Nr2@sms.bs.ch;

Beispiel:
SERVER = 'MYSERVER'
DATABASE = 'test'
INTERVAL = 60
PATH = '\\\\bs.ch\\dfs\\bs\\PD\\PD-StatA\\upload\\'
VERTEILER = '+41791742111@sms.bs.ch' # ;+41791742112@sms.bs.ch

## Installation
Diese Befehle clonen das git repo und erstellen das virtual environment.
```
$ git clone https://github.com/lcalmbach/folder-watch.git
$ python -m venv env
$ pip install -r requirements.txt
```
Zudem sollten die Parameter: Verteiler, Interval, path in const.py angepasst werden.

## Starten
in const.py überprüfen ob der Verteiler stimmt 
```
> env\scripts\activate.bat
> (env) python app.py
```

## Logging
Alle festgestellten Differenzen werden per sms verschickt und in die Datei folder-watcher.log geloggt.