#!/bin/bash

# Zur Sicherheit, falls der User nicht genügend Rechte hat
sudo chown `whoami` -R  ~/.virtualenvs
sudo chown `whoami` -R /usr/local/lib/python3.4/site-packages
sudo chmod -R 777 ~/.virtualenvs
sudo chmod -R 777 /usr/local/lib/python3.4/site-packages

# virtuelenvwrapper Script einlesen um desssen Befehle ausführen zu können
source "/usr/local/bin/virtualenvwrapper.sh"

# Eine neue virtuelle Umgebungen erstellen
mkvirtualenv grp_dev
deactivate

# Konfigurieren der virtuellen Umgebung

# SECRET_KEY erstellen
dir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
chmod +x $dir/python/random_string.py
secret_key=$(python $dir/python/random_string.py)

cd ~/.virtualenvs/grp_dev/bin
echo "unset GRPALLOC_DEBUG" >> predeactivate
echo "unset DJANGO_SETTINGS_MODULE='grpalloc.settings'" >> predeactivate
echo "unset GRPALLOC_SECRET_KEY" >> predeactivate
echo "export GRPALLOC_DEBUG = True" >> postactivate
echo "export DJANGO_SETTINGS_MODULE='grpalloc.settings'" >> postactivate
echo "export GRPALLOC_SECRET_KEY='$secret_key'" >> postactivate


echo "-------------------------------------------------------------
Mercurial installieren und konfigurieren
-------------------------------------------------------------"
read -p "Studentisches Kuerzel für Mercurial eingeben: " username

sudo apt-get -y install mercurial

# hgrc Datei für Mercurial erstellen 
# den username (wird beim pushen angezeigt) hinzufügen
# den Fingerprint hinzufügen, sonst kann keine Verbindung aufgebaut werden
touch ~/.hgrc
echo "[ui]
# Name data to appear in commits
username = $username

[hostfingerprints]
projekte.win.hs-heilbronn.de = e3:b8:ff:1e:b3:17:73:0a:d9:c0:8f:23:01:c3:63:2d:4c:fa:b8:47" >> ~/.hgrc


echo "-------------------------------------------------------------
Projekt klonen
-------------------------------------------------------------"

cd ~/Desktop
hg clone https://$username@projekte.win.hs-heilbronn.de/hg/grp/
cd grp

echo "-------------------------------------------------------------
Grundlegende Packages in den virt. umgebungen installieren und Datenbank anlegen
-------------------------------------------------------------"

workon grp_dev
pip3 install --upgrade --force-reinstall -r requirements.txt

# Datenbank migrieren
python manage.py migrate
# my_chache_table anlegen für den async task der Berechnung
python manage.py createcachetable

echo "-------------------------------------------------------------
Superuser anlegen
-------------------------------------------------------------"

python manage.py superuser

echo "-------------------------------------------------------------
Starten der Anwendung
-------------------------------------------------------------"

# open 2 (hold) terminal, 1 for the qcluster and 1 for the server
cd $dir/shell
chmod +x runserver.sh
chmod +x qcluster.sh
gnome-terminal --window-with-profile=hold -e ./runserver.sh
gnome-terminal --window-with-profile=hold -e ./qcluster.sh

sleep 5

# open the site
python3.4 -mwebbrowser http://127.0.0.1:8005

sleep 10

echo "-------------------------------------------------------------
Fertig. Dieses Terminal kann geschlossen werden!
-------------------------------------------------------------"

