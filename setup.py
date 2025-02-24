# !/usr/bin/python
# -*- coding: utf-8 -*-
#
##################################################################################
#
#    Copyright 2016-2018 Félix Brezo and Yaiza Rubio
#
#    This file is part of OSRFramework. You can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##################################################################################


import os
import sys
from setuptools import setup, find_packages
import shutil
import site


HERE = os.path.abspath(os.path.dirname(__file__))

# Importing the temporal scripts for the setup and taking the new version number
import osrframework
NEW_VERSION = osrframework.__version__

import osrframework.utils.configuration as configuration

# Depending on the place in which the project is going to be upgraded
try:
    raise Exception('Trying to load the markdown manually!')
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("[!] pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()
except Exception:
    read_md = lambda f: open(f, 'r').read()

# Reading the .md file
try:
    long_description = read_md(os.path.join(HERE,"README.md"))
except:
    long_description = ""

# Creating the application paths
paths = configuration.getConfigPath()

print("[*] Launching the installation of the osrframework module...")
# Launching the setup
setup(
    name="osrframework",
    version=NEW_VERSION,
    description="OSRFramework - A set of GPLv3+ OSINT tools developed by i3visio analysts for online research.",
    author="Felix Brezo and Yaiza Rubio",
    author_email="contacto@i3visio.com",
    url="http://github.com/i3visio/osrframework",
    license="COPYING",
    keywords = "python osint harvesting profiling username socialmedia forums",
    entry_points={
        'console_scripts': [
            'alias_generator = osrframework.alias_generator:main',
            'alias_generator.py = osrframework.alias_generator:main',
            'domainfy = osrframework.domainfy:main',
            'domainfy.py = osrframework.domainfy:main',
            'entify = osrframework.entify:main',
            'entify.py = osrframework.entify:main',
            'enumerate-profiles = osrframework.enumeration:main',
            'enumerate-profiles.py = osrframework.enumeration:main',
            'checkfy = osrframework.checkfy:main',
            'checkfy.py = osrframework.checkfy:main',
            'mailfy = osrframework.mailfy:main',
            'mailfy.py = osrframework.mailfy:main',
            'phonefy = osrframework.phonefy:main',
            'phonefy.py = osrframework.phonefy:main',
            'searchfy = osrframework.searchfy:main',
            'searchfy.py = osrframework.searchfy:main',
            'usufy = osrframework.usufy:main',
            'usufy.py = osrframework.usufy:main',
            'osrf = osrframework.launcher:main',
            'osrframework-cli = osrframework.launcher:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Telecommunications Industry',
        'Natural Language :: English',
        'Topic :: Communications',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
    packages=find_packages(),
    long_description=long_description,
    install_requires=[
        "setuptools",
        "mechanize",
        "BeautifulSoup",
        "requests",
        "python-emailahoy",
        "pyexcel==0.2.1",
        "pyexcel_ods==0.1.1",
        "pyexcel_xls==0.1.0",
        "pyexcel_xlsx==0.1.0",
        "pyexcel_io==0.1.0",
        "pyexcel_text==0.2.0",
        "tweepy",
        "networkx==2.2",
        "decorator",
        "validate_email",
        #"pydns",
        # Python3
        #"py3dns",
        #"robobrowser",
        "tabulate",
        "oauthlib>=1.0.0",
        "importlib",
        #"inspect",
        #"pkgutil",
        # Adding dependencies to avoid the InsecurePlatformWarning when calling Twitter API dealing with SSL: <http://stackoverflow.com/a/29202163>. Other options would require the user to upgrade to Python 2.7.9.
        #"pyopenssl",
        #"ndg-httpsclient",
        #"pyasn1"
        "python-whois",
        "pyyaml",
        "colorama",
        "configparser",
        "cfscrape"
    ],
)

############################
### Creating other files ###
############################
print("[*] Changing permissions of the user folders...")
try:
    configuration.changePermissionsRecursively(paths["appPath"], int(os.getenv('SUDO_UID')), int(os.getenv('SUDO_GID')))
except:
    # Something happened with the permissions... We omit this.
    pass

print("[*] Copying relevant files...")
files_to_copy= {
    paths["appPath"] : [
        os.path.join("config", "browser.cfg"),
        os.path.join("config", "general.cfg"),
    ],
    paths["appPathDefaults"] : [
        os.path.join("config", "accounts.cfg"),
        os.path.join("config", "api_keys.cfg"),
        os.path.join("config", "browser.cfg"),
        os.path.join("config", "general.cfg"),
    ],
    paths["appPathWrappers"] : [
        os.path.join("config", "plugins", "wrapper.py.sample"),
        os.path.join("config", "plugins", "wrapper_v2.py.sample"),
    ],
    paths["appPathPatterns"] : [
        os.path.join("config", "plugins", "pattern.py.sample"),
    ]
}

# Iterating through all destinations to write the info
for destiny in files_to_copy.keys():
    # Grabbing each source file to be moved
    for sourceFile in files_to_copy[destiny]:
        fileToMove = os.path.join(HERE,sourceFile)

        cmd = ""
        # Choosing the command depending on the SO
        if sys.platform == 'win32':
            if os.path.isdir(fileToMove):
                cmd = "echo d | xcopy \"" + fileToMove + "\" \"" + destiny + "\" /s /e"
            else:
                cmd = "copy \"" + fileToMove + "\" \"" + destiny + "\""
        elif sys.platform == 'linux2' or sys.platform == 'darwin':
            if not os.geteuid() == 0:
                cmd = "cp -r -- \"" + fileToMove + "\" \"" + destiny + "\""
            else:
                cmd = "sudo cp -r -- \"" + fileToMove + "\" \"" + destiny + "\""
        output = os.popen(cmd).read()
