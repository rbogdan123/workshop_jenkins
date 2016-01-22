#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

if __name__ == "__main__":
    here = os.path.abspath(".")
    # CHANGES = open(os.path.join(here, 'CHANGELOG')).read()

    setup(
        name="gruppeneinteilung",
        description="Web Application to execute Guppeneinteilung",
        version='0.0.1',
        packages=find_packages(),
        package_data={
            '': ['../*.txt',
                 '../*.py',
                 '../*.ini',
                 '../*.cfg',
                 '../scripts/**/*.py',
                 '../scripts/**/*.txt',
                 '../scripts/**/*.sh',
                 '../scripts/**/**/*.py',
                 '../scripts/**/**/*.sh',
                 '../documentation/*.docx',
                 '../documentation/*.pptx',
                 '../documentation/*.pdf',
                 'core/templates/*.html',
                 'core/templates/*.txt',
                 'core/templates/**/*.html',
                 'core/static/*.png',
                 'core/static/*.xml',
                 'core/static/*.ico',
                 'core/static/**/*.png',
                 'core/static/**/*.css',
                 'core/static/**/*.js',
                 'core/static/**/*.eot',
                 'core/static/**/*.svg',
                 'core/static/**/*.ttf',
                 'core/static/**/*.woff',
                 'core/static/**/**/*.js',
                 'core/static/**/**/*.png']
        },
        install_requires=[
            "arrow==0.7.0",
            "blessed==1.14.1",
            "Django==1.8.5",
            "django-picklefield==0.3.2",
            "django-q==0.7.11",
            "future==0.15.2",
            "pygal==2.0.11",
            "pyparsing==2.0.7",
            "python-dateutil==2.4.2",
            "six==1.10.0",
            "wcwidth==0.1.5",
            "wheel==0.26.0",
        ],
        license="CC BY-NC-SA 3.0 DE",
        url="http://projekte.win.hs-heilbronn.de/ps/grp",
        maintainer="Oliver Huettner",
        maintainer_email="huettner@stud.hs-heilbronn.de",
        keywords="teambuilding",
        classifiers=[
            "Development Status :: 1 - Planning",
            "Environment :: Web Environment",
            "Framework :: Django",
            "Intended Audience :: Lecture Team",
            "License :: OSI Approved :: Creative Commons License",
            "Programming Language :: Python :: 3.4",
            "Topic :: Teambuilding",
        ],
    )
