# TeleGiphy

## Overview
TeleGiphy is based off the icebreaker game, “Telephone”, where an original message 
is passed along a chain of players through whispers, and is entertaining through 
the often very distorted message at the end. 

TeleGiphy is a spin-off of the game that relies on Giphy’s magnificent random-ness 
when selecting gifs instead of whispers to distort messages. 

## Installing for development

1. Clone repo
1. Python 3.4+ required
1. Install virtualenv and virtualenvwrapper `pip install virtualenv virtualenvwrapper`

```bash
$ mkvirtualenv tele-giphy -p $(which python3)
$ echo "export OLD_PYTHONPATH=\${PYTHONPATH}" >> $WORKON_HOME/tele-giphy/bin/postactivate
$ echo "export DJANGO_SETTINGS_MODULE=tele_giphy.settings.local" >> $WORKON_HOME/tele-giphy/bin/postactivate
$ echo "export PYTHONPATH=tele_giphy:\${PYTHONPATH}" >> $WORKON_HOME/tele-giphy/bin/postactivate
$ echo "unset DJANGO_SETTINGS_MODULE" >> $WORKON_HOME/tele-giphy/bin/postdeactivate 
$ echo "export PYTHONPATH=\${OLD_PYTHONPATH}" >> $WORKON_HOME/tele-giphy/bin/postdeactivate 
$ echo "unset OLD_PYTHONPATH" >> $WORKON_HOME/tele-giphy/bin/postdeactivate
$ pip install -r requirements/local.txt
$ django-admin migrate
```

## Running the server

```bash
$ django-admin runserver
```

If you are on C9
```bash
$ django-admin runserver $IP:$PORT
```
