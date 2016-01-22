#!/bin/bash
source "/usr/local/bin/virtualenvwrapper.sh"
workon grp_dev
cd ~/Desktop/grp
python manage.py qcluster
