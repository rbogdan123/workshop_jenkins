#!/bin/bash
echo "-------------------------------------------------------------
Dieses Script installiert alle wichtigen Bestandteile, damit
Sie die GRP Website auf ihrem Linux-System (nur auf Ubuntu 14.04.3 getestet) läuft.
Zusammangefasst wird folgendes installiert:
* Python 3.4 und pip3
* virtualenv und virtualenvwrapper
* Konfiguration dieser beiden 
* Zwei virtuelle Umgebungen (grp_test und grp_dev) erstellen
* Mercurial installieren
* Projekt klonen und auf dem Desktop speichern
* Packages der requirements.txt installieren
* Datenbank migrieren
* Cachetable anlegen

Voraussetzungen
* ca. 120MB freier Festplattenspeicher

Notwendige Eingaben:
* Studentisches Kürzel (Für Mercurial)
* Password zu ihres HHN Accounts (Für Mercurial)
* Passwort ihres Rechners (Für sudo-Befehle)

Je nach Rechnerleistung und Internetgeschwindikeit dauert die
Installation bis zu 15 Minuten 
-------------------------------------------------------------"

echo "-------------------------------------------------------------
Notwendige Packages installieren
-------------------------------------------------------------"
sudo apt-get -y install build-essential python3-setuptools zlib1g-dev libssl-dev libsqlite3-dev sqlite3 apache2 apache2-utils libapache2-mod-wsgi-py3 zip libbz2-dev

echo "-------------------------------------------------------------
Python 3.4.3 und Pip3 installieren
-------------------------------------------------------------"
cd ~/Downloads/
wget http://python.org/ftp/python/3.4.3/Python-3.4.3.tgz
tar -xvf Python-3.4.3.tgz
cd Python-3.4.3
./configure
make
sudo make install
cd ..
rm -f ~/Downloads/Python-3.4.3.tgz
sudo rm -r -f ~/Downloads/Python-3.4.3
sudo pip3 install --upgrade pip

# turn on bash for autocomplete
pip3 completion --bash >> ~/.bashrc

# virtualenv & virtualenvwrapper installieren
echo "-------------------------------------------------------------
virtualenv & virtualenvwrapper installieren und konfigurieren
-------------------------------------------------------------"

# Pfad der Python3.4 Libraries
lib_dir=$(python3.4 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
# Pfad der Python3.4 bin
python_path="$(which python3.4)"

# set the Python Libraries as Pythonpath to the bashrc
echo "export PYTHONPATH=\$PYTHONPATH:$lib_dir" >> ~/.bashrc

# easy_install wurde automatisch mit py3.4 installiert, auch mit pip3 möglich
sudo python3.4 -m easy_install virtualenv
sudo python3.4 -m easy_install virtualenvwrapper

# virtualenv und virtualenvwrapper konfigurieren
mkdir ~/.virtualenvs
echo "export WORKON_HOME=~/.virtualenvs" >> ~/.bashrc
echo "export PIP_VIRTUALENV_BASE=~/.virtualenvs" >> ~/.bashrc
echo "export VIRTUALENVWRAPPER_PYTHON=$python_path" >> ~/.bashrc
echo "export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv" >> ~/.bashrc
echo "export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

# make next script executable
chmod +x setup_part2.sh

# `source ~/.bashrc` kann nicht in einem Script ausgeführt werden
echo "-------------------------------------------------------------

Führen Sie nun folgende Befehle aus:

source ~/.bashrc

./setup_part2.sh

-------------------------------------------------------------"
