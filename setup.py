#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
from geniusbot.version import __version__, __author__
from pathlib import Path
import re
import os
import sys
import sysconfig
if sys.platform == 'win32':
    from win32com.client import Dispatch

readme = Path('README.md').read_text()
version = __version__
readme = re.sub(r"Version: [0-9]*\.[0-9]*\.[0-9][0-9]*", f"Version: {version}", readme)
print(f"README: {readme}")
with open("README.md", "w") as readme_file:
    readme_file.write(readme)
description = 'Synchronize your subtitle files by shifting the subtitle time (+/-)'


# # Creates a Desktop shortcut to the installed software
# def post_install():
#     # Package name
#     packageName = 'Genius Bot'
#
#     # Scripts directory (location of launcher script)
#     scriptsDir = sysconfig.get_path('scripts')
#
#     # Target of shortcut
#     target = os.path.join(scriptsDir, packageName + '.exe')
#
#     # Name of link file
#     linkName = packageName + '.lnk'
#
#     # Read location of Windows desktop
#     desktopFolder = f"{Path.home()}/Desktop"
#
#     # Path to location of link file
#     pathLink = os.path.join(desktopFolder, linkName)
#     shell = Dispatch('WScript.Shell')
#     shortcut = shell.CreateShortCut(pathLink)
#     shortcut.Targetpath = target
#     shortcut.WorkingDirectory = scriptsDir
#     shortcut.IconLocation = target
#     shortcut.save()

setup(
    name='geniusbot',
    version=f"{version}",
    description=description,
    long_description=f'{readme}',
    long_description_content_type='text/markdown',
    url='https://github.com/Knucklessg1/subsync',
    author=__author__,
    author_email='knucklessg1@gmail.com',
    license='Unlicense',
    packages=[
        'geniusbot',
        'chatterbot',
        'chatterbot.storage',
        'chatterbot.logic',
        'chatterbot.ext',
        'chatterbot.ext.sqlalchemy_app',
    ],
    include_package_data=True,
    install_requires=['webarchiver', 'subshift', 'pandas', 'PyQt5', 'youtube-dl', 'en_core_web_sm', 'sqlalchemy',
                      'pytz', 'python-dateutil', 'mathparse',],
    dependency_links=[
        'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.3.0/en_core_web_sm-3.3.0.tar.gz#egg=en_core_web_sm'
    ],
    py_modules=['geniusbot'],
    package_data={'geniusbot': ['geniusbot']},
    data_files=[("geniusbot",  ["geniusbot/img/geniusbot.ico", "geniusbot/img/geniusbot.png"])],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: Public Domain',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={'console_scripts': ['geniusbot = geniusbot.geniusbot:main']},
)

# if sys.argv[1] == 'install' and sys.platform == 'win32':
#     post_install()
