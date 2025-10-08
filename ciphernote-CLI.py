#python

#File:        ciphernote-CLI.py
#Author:      u112000
#Created:     2025-10-08

#License:     MIT License — see LICENSE file in repository
#Repository:  https://github.com/u112000

import os
import sys
import time
import sqlite3
from rich import print
from package import core

p =f'''

[dim]========================================================[/dim]
            🔐 [bold cyan]C I P H E R   [dim]_[/dim]   N O T E[/bold cyan]
[dim]========================================================[/dim]



{core.info} Welcome, modules loaded successfully.'''

def Database_initialization():
    try:
        print(f'{core.info} Preparing Database..')
        connection = sqlite3.connect(core.dbase)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS notes_DB (
              id INTEGER PRIMARY KEY,
              date TEXT NOT NULL,
              title TEXT NOT NULL,
              entry TEXT NOT NULL UNIQUE,
              tags TEXT NOT NULL,
              mood INTEGER NOT NULL,
              encryptionStatus NOT NULL)
                       ''')
        connection.commit()
        cursor.close()
        connection.close()
        time.sleep(3)
    except:
        print(f'{core.critic} Unable to create sqlite3 database\nSQLITE3 RELATED ERROR!', end='')
        sys.exit()

def functionalitycheck():
    print(f'{p}')
    if os.path.exists('./package') != True:
        print(f'{core.critic}Missing core path detected!\n')
        raise Exception('Error core dictionary missing.\nLikely due to incomplete download.')

    if os.path.exists('./logs') != True:
        print(f'{core.info} Missing path "logs". creating folder..')
        time.sleep(2)
        try: os.mkdir('./logs')
        except:
            print(f'{core.critic} Unable to create required folder "./logs" \n')
            raise Exception('DICT WRITE PRIVILEGE ERROR')

    if os.path.exists('./database') != True:
        print(f'{core.warning} Missing path "database". creating folder.')
        time.sleep(2)
        try:
            os.mkdir('./database')
        except:
            print(f'{core.critic} Unable to create required folder "./database"\n')
            raise Exception('DICT WRITE PRIVILEGE ERROR')
    if os.path.isfile(core.dbase) != True or os.stat(core.dbase).st_size == 0:
        Database_initialization()

functionalitycheck()
time.sleep(3)
core.main_screen()

