#python

#File:        core.py
#Author:      u112000
#Created:     2025-10-08

#License:     MIT License — see LICENSE file in repository
#Repository:  https://github.com/u112000

# BLESS THIS MESS
# DONT MIND ME    :)

import sys
import os
import time
import json
import sqlite3
import secrets
import fortune  # pip install fortune-python
from rich import print
from random import randint
#from matplotlib import pyplot
from package.encryption_admin import *


date_month_year_time = f'{time.strftime("%d-%m-%Y %I:%M %p", time.localtime())}'
month_year = f'{time.strftime("%B %Y", time.localtime())}'
dbase = './database/notebook.db'

info = '[[bold white]INFO[/bold white]]'
success = '[[bold green]SUCCESS[/bold green]]'
warning = '[[bold yellow]WARNING[/bold yellow]]'
inter = '[[bold red]INTERRUPT[/bold red]]'
critic = '[[bold red]CRITICAL[/bold red]]'
debug = '[[bold cyan]DEBUG[/bold cyan]]'

def Searcher():
    print(f"{info}🔎 Please Enter A Search keyword: ", end='')
    try:
        respond = Input_Validator(input())
    except KeyboardInterrupt:
        print(f"{inter}[red]⚠️ Please Use '[bold white]exit/q[/bold white]' Next Time To Quit Gracefully.[/red]")
        logger(f"[CRITICAL] Search operation cancelled by user via keyboard interrupt. ended program")
        sys.exit()
    else:
        connection = sqlite3.connect(dbase)
        cursor = connection.cursor()
        damn_it = cursor.execute('SELECT id, title, entry, tags, encryptionStatus FROM notes_DB')
        if damn_it == []:
            print(f"{info} No notes currently saved. Create a note before searching.")
            cursor.close()
            connection.close()
            main_screen()
        found_targets = []
        for i in damn_it:
            if respond in i[1] or respond == i[1]:
                if i not in found_targets:
                    found_targets.append(i)
            elif respond in i[2] or respond == i[2]:
                if i not in found_targets:
                    found_targets.append(i)
            elif respond in i[3] or respond == i[3]:
                if i not in found_targets:
                    found_targets.append(i)
            else:
                continue
        if found_targets == []:
            print(f"{warning} No results found for: '{respond}'.")
            cursor.close()
            connection.close()
            logger(f"[WARNING] User attempt searching for {respond} failed!, Due to no similar word!")
            main_screen()
        else:
            print(f"{success}✅ Matches Detected:\n")
            for i in found_targets:
                print(r' ──────────────────────────────')
                print(f'| FILE ID..............[ {i[0]} ]')
                print(r'| ENCRYPTION...........[ '+ DRY(f'{i[4]}') +' ]')
                print(f'| TITLE................[ {i[1][:25]}**** ]')
                print(f'| TAGS.................[ {i[3]} ]\n')
                print(r' ──────────────────────────────')
                print(f' ENTRY CONTENT ::\n')
                print(f'> {i[2][:50]}****')
                print(f' ───────────────────────────────\n\n')
            cursor.close()
            connection.close()
            logger(f"[SUCCESS] Keyword: '{respond}', returned {len(found_targets)} result(s).")
            Menu()

def DRY(n):
    if n == 'NOT-ENCRYPTED':
        return f"[bold blue]{n}[/bold blue]"
    else:
        return f"[bold red]{n}[/bold red]"

def Viewnote():
    print(f"{info}📝 Enter the Note ID to view: ", end='')
    try:
        respond = Input_Validator(input())
    except KeyboardInterrupt:
        print(f"{inter}⚠️ Please use '[bold white]exit/q[/bold white]' next time to quit gracefully.")
        logger(f"[CRITICAL] View note operation cancelled by user. ended program")
        sys.exit()
    else:
        connection = sqlite3.connect(dbase)
        cursor = connection.cursor()
        cursor.execute('SELECT id, date, title, entry, tags, encryptionStatus FROM notes_DB WHERE id = ?', (respond,))
        damn_it = cursor.fetchall()
        if damn_it == []:
            print(f"{warning}❗ Note not found. Please verify the Note ID and try again.")
            cursor.close()
            connection.close()
            main_screen()
        else:
            print(r' ──────────────────────────────')
            print(f'| FILE ID..............[ {damn_it[0][0]} ]')
            print(f'| CREATED..............[ {damn_it[0][1]} ]')
            print(r'| ENCRYPTION...........[ '+DRY(f'{damn_it[0][5]}')+' ]')
            print(f'| TITLE................[ {damn_it[0][2][:30]} ]')
            print(f'| TAGS.................[ {damn_it[0][4]} ]\n')
            print(r' ──────────────────────────────')
            print(f' ENTRY CONTENT ::\n')
            print(f'> {damn_it[0][3]}')
            print('\n')
            print(f"[green]— END OF NOTE —[/green]".center(50, '='))
            print('\n')
            cursor.close()
            connection.close()
            logger(f"[INFO] Displayed note ID: {respond} to user.")
            Menu()


def SearchTag():
    a,b,c,d,e,f,g = ('personal', 'home', 'health', 'work','sensitive', 'creativity', 'others')
    print("""
 ⟡[bright_cyan] a[/bright_cyan]> [white]Personal[/white]
 ⟡[bright_cyan] b[/bright_cyan]> [white]Home[/white]
 ⟡[bright_cyan] c[/bright_cyan]> [white]Health[/white]
 ⟡[bright_cyan] d[/bright_cyan]> [white]Work[/white]
 ⟡[bright_cyan] e[/bright_cyan]> [white]Sensitive[/white]
 ⟡[bright_cyan] f[/bright_cyan]> [white]Creativity[/white]
 ⟡[bright_cyan] g[/bright_cyan]> [dim]Other(s)[/dim]
    """)
    print(f"{info}🔎 Pick a tag (e.g. 'g'): ", end='')
    try:
        respond = Input_Validator(input())
    except KeyboardInterrupt:
        print(f"{inter}⚠️ Please use '[bold white]exit/q[/bold white]' next time to quit gracefully.")
        logger(f"[CRITICAL] Tag search aborted by user.")
        sys.exit()
    else:
        if respond not in ('a', 'b', 'c', 'd', 'e', 'f', 'g'):
            print(f"{warning}⚠️ Invalid selection: '{respond}'. Please choose one of the listed options.")
            SearchTag()
        if respond == 'a': respond = a
        elif respond == 'b': respond = b
        elif respond == 'c': respond = c
        elif respond == 'd': respond = d
        elif respond == 'e': respond = e
        elif respond == 'f': respond = f
        elif respond == 'g': respond = g
        connection = sqlite3.connect(dbase)
        cursor = connection.cursor()
        damn_it = cursor.execute('SELECT id, title, tags, encryptionStatus FROM notes_DB')
        if damn_it == []:
            print(f"{warning} No notes currently saved. Create a note before searching by tag.")
            cursor.close()
            connection.close()
            main_screen()
        found_targets = []
        for i in damn_it:
            if respond in i[2] or respond == i[2]:
                if i not in found_targets:
                    found_targets.append(i)
            else:
                continue
        if found_targets == []:
            print(f"{warning} No notes found with the tag: '{respond}'.")
            cursor.close()
            connection.close()
            main_screen()
        else:
            print(f"{success}✅ Notes found with tag '{respond}': \n")
            for i in found_targets:
                print(r' ──────────────────────────────')
                print(f'| FILE ID..............[ {i[0]} ]')
                print(r'| ENCRYPTION...........[ '+DRY(f'{i[3]}')+' ]')
                print(f'| TITLE................[ {i[1][:25]}**** ]')
                print(f'| TAGS.................[ {i[2]} ]\n')
                print(' ──────────────────────────────\n')
            cursor.close()
            connection.close()
            logger(f"[INFO] Tag '{respond}' returned {len(found_targets)} result(s).")
            Menu()


def credit():
    print(f'''[green]
\t==================================================.
\t      |     | |       |             |     |   |   |
\t.===. '== | | | .== | | ==========. '=. | | .=' | |
\t|   |     | |   |   | |     |     |   | |   |   | |
\t| | '=====| | .=' .=' '==== | ==. '== | | .=' ==| |
\t| |     | | | |   |         |   |     | | |     | |
\t| '==== | | '=' .=+=============| .===| '=' .===| |
\t|   |   | |     | |             | |   |     |   | |
\t| | '=. | |=====' |             | | | | .===' | | |
\t| [/green][bold white]466f722074686520637572696f7573206d696e64732e2e[/bold white][green]  |
\t| | | | | | .=' | |             | .=======' | ==| |
\t| |   |   | |   | |             | |   |     |   | |
\t| '=. |===| | ==| '=============' | | | ======= | |
\t|   | |   | |   |   |     |         |     |     | |
\t| | '=| | | '=. |===' .== | ========+=====' | .=' |
\t| |   | | |   | |     |   |   |     | |     | |   |
\t| '=. | | '== | | ====| ===== | .== | | ======' =='
\t|   | |   |     |       |         |     |
\t'==================================================[/green]

If you enjoyed this project, please consider giving it a ⭐ on the
repo: https://github.com/u112000. If you'd like to support development,
consider buying a cup of coffee. ☕

[underline]bitcoin[/underline]: [bold grey]bc1qp586f6zvyh3r8qe78tvxh0mstr7sn09gqw7lfk[/bold grey]
[underline]monero[/underline]: [bold grey]436ynu4GtAfDdHn2noch5fBC1ohiFwuiB6YpTKokt5SoQEttSSxsFEBiZNim8T5QJo1BzFJ54FkQwN2oFtP8Lxau39GvQbY[/bold grey]
             ''')
    Menu()

def List_Out():
    try:
        connection = sqlite3.connect(dbase)
        cursor = connection.cursor()
    except:
        print(f"{critic} Unable to access the SQLite database.", end='')
        logger(f"[CRITICAL] Database interatcion problem. maybe missing module?. program ended")
        sys.exit()
    else:
        cursor.execute('SELECT id, date, title FROM notes_DB')
        requested_data = cursor.fetchall()
        if requested_data == []:
            print(f"{warning} No entries found in the database.")
            cursor.close()
            connection.close()
            Menu()
        else:
            time.sleep(1)
            max_date_len = 25
            max_title_len = 40
            max_id_len = 15
            truncated_data = [
                (
                    str(i[0])[:max_id_len] + ('...' if len(str(i[0])) > max_id_len else ''),
                    i[1][:max_date_len] + ('...' if len(i[1]) > max_date_len else ''),
                    i[2][:max_title_len] + ('...' if len(i[2]) > max_title_len else '')
                  )
                for i in requested_data
                ]
            date_width = max(len(i[1]) for i in truncated_data)
            title_width = max(len(i[2] + '***') for i in truncated_data)
            id_width = max(len(str(i[0])) for i in truncated_data)
            print(f"\n| {'Date Created':<{date_width}} | {'Title':<{title_width}} | {'ID No':<{id_width}}")
            print(f"|{'='*date_width}= | {'='*title_width} | {'='*id_width}")
            for i in truncated_data:
                print(f"| {i[1]:<{date_width}} | {i[2]:<{title_width}} | {i[0]:<{id_width}}")
            print('')
            cursor.close()
            connection.close()
            logger(r"[INFO] User listed all notes from the database.")
            Menu()

def graph():
    connection = sqlite3.connect(dbase)
    cursor = connection.cursor()
    cursor.execute('SELECT date, mood FROM notes_DB')
    raw_chart_data = cursor.fetchall()
    x = []
    y = []
    for i in raw_chart_data:
        x.append(i[0][:10])
        y.append(i[1])
    cursor.close()
    connection.close()
    pyplot.style.use('ggplot')
    pyplot.plot(x, y, marker='s', label='mood')
    pyplot.legend()
    pyplot.grid(True, axis='y')
    pyplot.xticks(rotation=90)
    pyplot.title('MOOD ANALYSIS')
    pyplot.xlabel('Mood')
    pyplot.ylabel('Dates')
    pyplot.show()
    filepath = f'./{time.strftime("%d_%m_%Y_%I-%M%P", time.localtime())}.pdf'
    pyplot.savefig(filepath)
    print(f"{success}✅ Chart exported to: [bold green]{filepath}[/bold green]")
    main_screen()

def Locker():
    print(f"{info}📝 Enter the Note ID to ENCRYPT: ", end='')
    try:
        respond = Input_Validator(int(input()))
    except KeyboardInterrupt:
        print(f"{critic}⚠️ Please use '[bold white]exit/q[/bold white]' next time to quit gracefully.")
        logger(f"[CRITICAL] Attempted Encrypting a note, but program cancelled by user. program ended")
        sys.exit()
    except ValueError:
        print(f'{warning}Invalid input! INTEGER(s) required.')
        time.sleep(3)
        Locker()
    else:
        connection = sqlite3.connect(dbase)
        cursor = connection.cursor()
        data = cursor.execute('SELECT title, entry, encryptionStatus FROM notes_DB WHERE id = ?', (respond,)).fetchall()
        if len(data) != 0:
            if data[0][2] == 'ENCRYPTED':
                os.system('cls' if os.name == 'nt' else 'clear')
                print("""
\t\t[bold white]> [/bold white][bold magenta]!!Immediate Attention Required!![/bold magenta] [bold white]<[/bold white]
> This note data is protected from disclosure and [bold red]secured by AESGCM encryption[/bold red].
> Readability is hereby restricted, and this program is 
> unable to [bold red]re-encrypt[/bold red] an [bold red]encrypted[/bold red] data!
""")
                cursor.close()
                connection.close()
                Menu()

            time.sleep(2)
            encryted_response = encryptor(data[0][0], data[0][1], data[0][2], 's')
            cursor.execute('UPDATE notes_DB SET title = ?, entry = ?, encryptionStatus = ? WHERE id = ?', (encryted_response[0], encryted_response[1], encryted_response[2], respond))
            connection.commit()
            cursor.close()
            connection.close()
            logger(f"[INFO] Encrypted note ID N0- {respond} successfully")

            os.system('cls' if os.name == 'nt' else 'clear')
            print("[bold red]SECURITY NOTICE[/bold red]")
            print("[yellow]-----------------------------------------------[/yellow]")
            print("[bold green]ENCRYPTION PROCESS: SUCCESSFULLY COMPLETED[/bold green]")
            print("[yellow]-----------------------------------------------[/yellow]\n")

            print("[bold red]CAUTION:[/bold red] This information is highly sensitive.")
            print("Losing these keys will result in [bold red]PERMANENT DATA LOSS[/bold red].")
            print("Store them in a [underline]secure, offline location/file[/underline].\n")

            print(f"[cyan]ENCRYPTION KEY:[/cyan] [white]{encryted_response[3]}[/white]")
            print(f"[cyan]NONCE / IV:[/cyan] [white]{encryted_response[4]}[/white]")
            print(f"[cyan]AAD KEY:[/cyan] [white]{encryted_response[5]}[/white]\n")

            print("[dim]STORE THESE VALUES SECURELY AND DO NOT SHARE THEM[/dim]")
            print("[dim]AS THESE KEY WOULD ASLO BE USED IN DECRYPTION![/dim]\n[white]ENTER 'clear' TO CLEAR SCREEN![white]\n")
            Menu()
        elif len(data) == 0:
            cursor.close()
            connection.close()
            print(f"{warning} No notes found with the ID N0-: '{respond}'.")
            logger(f"[WARNING] Attempted Encrypting a note, But failed due to Note ID no-'{respond}' not found")
            main_screen()
_key = ''
_nonce = ''
_aad = ''
def Lockall():
    global _key, _nonce, _aad
    print(f"{info} [bold yellow]Confirmation required:[/bold yellow] [white]Are you certain you want to encrypt all notes?[/white]")
    print(f"{info} [bold green]'yes'[/bold green] to continue or [bold red]'no'[/bold red] to decline: ", end='')
    try:
        respond = Input_Validator(input())
    except KeyboardInterrupt:
        print(f"{inter}⚠️ Please use '[bold white]exit/q[/bold white]' next time to quit gracefully.")
        logger(f"[CRITICAL] Attempted Encrypting a note, but program cancelled by user. program ended")
        sys.exit()
    except ValueError:
        print(f'{warning} Invalid input! INTEGER(s) required.')
        time.sleep(3)
        Lockall()
    else:
        if respond not in ('yes', 'no'):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'''
   !!{info}!!______________________________________________
  
 • For urgent verification purposes, please ensure your response is 
 • limited to either [green]"YES"[/green] / [red]"NO"[/red]. Any other input will be considered 
 • invalid. Please confirm your answer accordingly.
''')

            Lockall()
        elif respond == 'yes':
            _key = secrets.token_bytes(32)
            _nonce = secrets.token_bytes(12)
            _aad = secrets.token_bytes(12)

            connection = sqlite3.connect(dbase)
            cursor = connection.cursor()
            data = cursor.execute('SELECT id, title, entry, encryptionStatus FROM notes_DB').fetchall()
            if len(data) == 0:
                cursor.close()
                connection.close()
                print(f"{warning} No notes saved yet!'.")
                logger(f"[WARNING] Attempted Encrypting all note, But failed due to zero notes in DB")
                main_screen()
            elif len(data) != 0:
                for i in data:
                   if i[3] == 'NOT-ENCRYPTED':
                        output = encryptor(i[1], i[2], i[3], 'a')
                        cursor.execute('UPDATE notes_DB SET title = ?, entry = ?, encryptionStatus = ? WHERE id = ?',(output[0], output[1], output[2], i[0]))
                   else: continue
                os.system('cls' if os.name == 'nt' else 'clear')
                print("[bold red]MAJOR SECURITY NOTICE[/bold red]")
                print("[yellow]-----------------------------------------------[/yellow]")
                print("[bold green]MASS ENCRYPTION PROCESS: SUCCESSFULLY COMPLETED[/bold green]")
                print("[yellow]-----------------------------------------------[/yellow]\n")
                print("[bold red]CAUTION:[/bold red] This information is highly sensitive.")
                print("Losing these keys will result in [bold red]PERMANENT DATA LOSS[/bold red].")
                print("Store them in a [underline]secure, offline location/file[/underline].\n")

                print(f"[cyan]ENCRYPTION KEY:[/cyan] [white]{_key.hex()}[/white]")
                print(f"[cyan]NONCE / IV:[/cyan] [white]{_nonce.hex()}[/white]")
                print(f"[cyan]AAD KEY:[/cyan] [white]{_aad.hex()}[/white]\n")


                print("[dim]STORE THESE VALUES SECURELY AND DO NOT SHARE THEM[/dim]")
                print("[dim]AS THESE KEY WOULD ASLO BE USED IN DECRYPTION![/dim]\n[white]ENTER 'clear' TO CLEAR SCREEN![white]\n")
                connection.commit()
                cursor.close()
                connection.close()
                logger("[INFO] Mass notes encryption initiated")
                Menu()
        elif respond == 'no':
            Menu()

def Unlock(type):
    os.system('cls' if os.name == 'nt' else 'clear')
    notice = '''

  [bold cyan]Ensure that you input the precise details employed in the 
    encryption of this specific note. These particulars are essential 
  for accurate decryption and access.[/bold cyan]

    '''
    time.sleep(4)
    if type == 'S':
        print(f'{notice}\n\n')
        print(f'{info} Please enter/paste the encrypted note ID of interest')
        try:
            respond = Input_Validator(int(input('ID N0-: ')))
        except KeyboardInterrupt:
            print(f"{inter} Use '[bold white]exit/q[/bold white]' to quit at any time.")
            Menu()
        except ValueError:
            print(f'{warning} Invalid input! INTEGER(s) required.')
            Unlock('S')
        else:
            connection = sqlite3.connect(dbase)
            cursor = connection.cursor()
            data = cursor.execute('SELECT id, title, entry, encryptionStatus FROM notes_DB WHERE id = ?', (respond,)).fetchall()
            if len(data) == 0:
                cursor.close()
                connection.close()
                print(f"{warning} No notes exists with such ID {respond}!.")
                Menu()
            elif len(data) != 0:
                if data[0][3] == 'NOT-ENCRYPTED':
                    print(f"{warning} This note is [bold underline]NOT ENCRYPTED[/bold underline]!!")
                    print(f"{warning} You cannot decrypt a file that was never encrypted — such an action is both futile and illogical!\n")
                    cursor.close()
                    connection.close()
                    Menu()
                elif data[0][3] == 'ENCRYPTED':
                    try:
                        print("\n[bold red]Key:[/bold red] Please enter the key")
                        key_phrase = Input_Validator(input(r'[!] Key phrase: '))
                        print("\n[bold magenta]Nonce / IV:[/bold magenta] Please enter a correct nonce.")
                        nonce_phrase = Input_Validator(input(r'[!] Nonce: '))
                        print("\n[bold cyan]AAD (Associated Data):[/bold cyan] Please enter the AAD.")
                        aad_phrase = Input_Validator(input(r'[!] AAD: '))
                    except KeyboardInterrupt:
                        print(f"{inter} Use '[bold white]exit/q[/bold white]' to quit at any time.")
                        List_Out()
                    decrypted = Decryptor(key_phrase, nonce_phrase, aad_phrase, data[0][1], data[0][2])
                    if decrypted == 'ERROR':
                        print(f"{warning} Decryption failed! The process was terminated due to an incorrect value in one or more key phrases.")
                        print(f"{warning} The encryption mechanism (AESGCM)is extremely delicate — all keys must be [bold underline]100% accurate[/bold underline] for successful decryption!\n")
                        Menu()
                    elif decrypted != 'ERROR':
                        cursor.execute('UPDATE notes_DB SET title = ?, entry = ?, encryptionStatus = ? WHERE id = ?', (decrypted[0], decrypted[1], decrypted[2], respond))
                        connection.commit()
                        cursor.close()
                        connection.close()
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f"{info} [cyan]DATA RECOVERED SUCCESSFULLY[/cyan]\n")
                        print(f"{info} [dim]THIS NOTE IS NO LONGER ENCRYPTED![/dim]")
                        print(f"{info} [dim]USER CAN NOW SECURELY DELETE THE KEYS, AS ITS NO LONGER NEEDED[/dim]\n[white]ENTER 'clear' TO CLEAR SCREEN![white]\n")
                        Menu()
    elif type == 'M':
        print(f'{notice}\n\n')
        connection = sqlite3.connect(dbase)
        cursor = connection.cursor()
        data = cursor.execute('SELECT id, title, entry, encryptionStatus FROM notes_DB').fetchall()
        if len(data) == 0:
            cursor.close()
            connection.close()
            print(f"{warning} No notes exists yet!.")
            Menu()
        elif len(data) != 0:
            try:
                print(f"\n{info} [bold red]Key:[/bold red] Please enter the key") 
                key_phrase = Input_Validator(input(r'[!] Key phrase: '))
                print(f"\n{info} [bold magenta]Nonce / IV:[/bold magenta] Please enter a correct nonce.")
                nonce_phrase = Input_Validator(input(r'[!] Nonce: '))
                print(f"\n{info} [bold cyan]AAD (Associated Data):[/bold cyan] Please enter the AAD.")
                aad_phrase = Input_Validator(input(r'[!] AAD: '))
            except KeyboardInterrupt: 
                print(f"{inter} Use '[bold white]exit/q[/bold white]' to quit at any time.")
                List_Out()
            successful_decrypted = []
            failed_decryption = []

            for i in data:
                if i[3] == 'ENCRYPTED':
                    decrypted = Decryptor(key_phrase, nonce_phrase, aad_phrase, i[1], i[2])
                    if decrypted == 'ERROR':
                        failed_decryption.append(i[0])
                        continue
                    elif decrypted != 'ERROR':
                        cursor.execute('UPDATE notes_DB SET title = ?, entry = ?, encryptionStatus = ? WHERE id = ?', (decrypted[0], decrypted[1], decrypted[2], i[0]))
                        successful_decrypted.append(i[0])
                else: continue 
            if len(successful_decrypted) > 0:
                print(f"\n{info} [cyan]DATA RECOVERED SUCCESSFULLY[/cyan]\n")
                print(f"{info}[dim] [white]'{len(successful_decrypted)}'[/white] NOTES ARE NO LONGER ENCRYPTED![/dim]")
                print(f"{info} [dim]USER CAN NOW SECURELY DELETE THE KEYS, AS ITS NO LONGER NEEDED[/dim]\n[white]ENTER 'clear' TO CLEAR SCREEN[/white]\n")
                print(f'{info} SUCCESSFULL DECRYPTION: {len(successful_decrypted)}\n{warning} FAILED DECRYPTION: {len(failed_decryption)}\n')
                connection.commit()
                cursor.close()
                connection.close()
                Menu()
            elif len(successful_decrypted) == 0:
                print(f"\n{warning} [cyan]DATA RECOVERED[/cyan] [red]NOT SUCCESSFULLY[/red]\n")
                print(f"{warning} [dim]INABILITY TO REMEMBER THE KEY PHRASE, IS INABILITY TO RECOVER DATA!! [red]REVIEW KEYS IMMEDIATELY[/red][/dim]\n[white]ENTER 'clear' TO CLEAR SCREEN[/white]\n")
                print(f'{success} SUCCESSFULL DECRYPTION: {len(successful_decrypted)}\n{warning} FAILED DECRYPTION: {len(failed_decryption)}\n')
                connection.commit()
                cursor.close()
                connection.close()
                Menu()

def Menu():
    print(f"[*] [bold white]CipherNote_CLI[/bold white]> ", end="")
    try:
        respond = Input_Validator(input())
    except KeyboardInterrupt:
        print(f"{inter} Use '[bold white]exit/q[/bold white]' to quit at any time.")
        Menu()
    if respond == 'list': List_Out() #ok
    elif respond == 'create': Create() #ok
    elif respond == 'delete': Deleter() #ok
    elif respond == 'search': Searcher() #ok
    elif respond == 'searchtag': SearchTag() #ok
    elif respond == 'viewnote': Viewnote() #ok
    elif respond == 'help': main_screen() #ok
    elif respond == 'mood_graph': graph() #ok
    elif respond == 'exit': Input_Validator('EXIT') #ok
    elif respond == 'credits': credit() #ok
    elif respond == 'logs': Logger() #ok
    elif respond == 'clear': main_screen() #ok
    elif respond == 'lock': Locker() #ok
    elif respond == 'unlock': Unlock('S') #pk
    elif respond == 'lockall': Lockall() #ok
    elif respond == 'unlockall': Unlock('M') #ok
    else:
        print(f"{warning}❗ Command not found: [red]{respond}[/red]")
        Menu()


def Deleter():
    print(f"{info} Enter the Note ID to delete: ", end='')
    try:
        respond = Input_Validator(int(input()))
    except KeyboardInterrupt:
        print(f"{critic} Please use '[bold white]exit/q[/bold white]' next time to quit gracefully.")
        logger(f"[CRITICAL] Delete operation cancelled by user. Target ID: {respond}. program ended")
        sys.exit()
    except ValueError:
        print(f'{warning} Invalid input! INTEGER(s) required.')
        time.sleep(4)
        Deleter()
    connection = sqlite3.connect(dbase)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM notes_DB WHERE id = ?', (respond,))
    if cursor.fetchall() == []:
        print(f'{warning} Not found. Verify the ID or type exit to cancel.')
        logger(f"[WARNING] Attempted to delete ID '{respond}' but it was not found.")
        Deleter()
    cursor.execute('DELETE FROM notes_DB WHERE id = ?', (respond,))
    print(f'{success} Note deleted successfully.')
    connection.commit()
    cursor.close()
    connection.close()
    logger(f"[SUCCESS] Note with ID '{respond}' was removed by user.")
    main_screen()

def Logger():
    log_json = {}
    connection = sqlite3.connect(dbase)
    cursor = connection.cursor()
    data = cursor.execute('SELECT * FROM logs_DB').fetchall()
    for i in data:
        log_json[i[0]] = [i[1]]
    f = open(f'./logs/{data[0][0]}_{data[-1][0]}.json', 'w')
    f.write(json.dumps(log_json))
    f.close()
    print(f'\n{info} Log file saved to ./logs/{data[0][0]}___{data[-1][0]}.json')
    cursor.close()
    connection.close()
    print(f'\n{info} ..Redirecting Back To Main Screen')
    time.sleep(4)
    main_screen()

def Create():
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n'+f'''
                          =======-
                    =================
              ========================
        ===============================
    ========================+++=========
  ++=================+++==-:=+===========
 @%##*+========++++=-:........+===========
%%#%%#*=======+=:.....:::......=+==========
 @@%#%#**=======:...............==+=========
  @@@%%***========:...[ [bold green]Note[/bold green] ]..=+=========
   %@%%%*++========-........:::::..=++=========
    @@%%%**=========-..::::....:....:=+=========
     %@@%%#*#=========:......::--:..:-=+=========
      %@@#%#**=========:.......:--================
       @@@#%*++========:.:--======================
        @@@%%*+=====================================
         @@%%%#*+====================================
          %@%%#**+====================================
           @@@%%#*++================================
            %@@%%*+================================
             %@%%%#*+==========================++++====-
              %@%%#*#+=====================+++++=========
               @@@%%#++======================+========---
                %@@%%#*+==========================--=
                 %@%%###*=====================--
                  @@%%#***================-=+
                   @@@%%#*++===========-=
                    %@@%%##*========+
                     %%@##+=====+
                      #**+#
                      :::
                      :::

    ''')
    time.sleep(1)
    print(f"\n{info} Enter Note Title (type 'exit/q' to cancel)")
    print(f"\n{info} [bold underline]NOTE TITLE[/bold underline]> ", end='')
    try:
        note_title = Input_Validator(input()) # note title
    except KeyboardInterrupt:
        print(f"{critic} Operation cancelled. program ended.")
        logger(f"[CRITICAL] Program ended? forcfully")
        sys.exit()
    print(f"\n{info} [bold underline]NOTE ENTRY/BODY[/bold underline]> ", end='')
    try:
        note_Entry = Input_Validator(input()) # note Entry
    except KeyboardInterrupt:
        print(f"{critic} Operation cancelled. Returning to main screen.")
        logger(f"[CRITICAL] Program ended? forcfully")
        sys.exit()
    print("""
[bold bright_yellow]
 ╔════════════════════════════════════════╗
 ║           [bold green]REGISTERED TAGS[/bold green]              ║
 ╚════════════════════════════════════════╝
[/bold bright_yellow]

 ⟡[bright_cyan] a[/bright_cyan]> [white]Personal[/white]
 ⟡[bright_cyan] b[/bright_cyan]> [white]Home[/white]
 ⟡[bright_cyan] c[/bright_cyan]> [white]Health[/white]
 ⟡[bright_cyan] d[/bright_cyan]> [white]Work[/white]
 ⟡[bright_cyan] e[/bright_cyan]> [white]Sensitive[/white]
 ⟡[bright_cyan] f[/bright_cyan]> [white]Creativity[/white]
 ⟡[bright_cyan] g[/bright_cyan]> [dim]Other(s)[/dim]
    """)
    a,b,c,d,e,f,g = ('personal', 'home', 'health', 'work','sensitive', 'creativity', 'others')
    try:
        print(f'{info} [bold underline]NOTE TAG[/bold underline]: ', end='')
        note_tag = Input_Validator(input()) # note tag
    except KeyboardInterrupt:
        print(f"{critic} Operation cancelled. Returning to main screen.")
        logger(f"[CRITICAL] Program ended? forcfully")
        sys.exit()
    if note_tag == 'a': note_tag = a
    elif note_tag == 'b': note_tag = b
    elif note_tag == 'c': note_tag = c
    elif note_tag == 'd': note_tag = d
    elif note_tag == 'e': note_tag = e
    elif note_tag == 'f': note_tag = f
    elif note_tag == 'g': note_tag = g
    else:
        print(f'{warning} Invalid selection detected. Default tag [bold]others[/bold] will be applied.')
        note_tag = g

    print(f'\n{info} Rate your mood today on a scale from 1 to 10,\n{info} where 1 = Very Negative, 10 = Very Positive: ', end='')
    try:
        note_mood = Input_Validator(int(input()))
    except KeyboardInterrupt:
        print(f"{critic} Operation cancelled. Returning to main screen.")
        logger(f"[CRITICAL] Program ended? forcfully")
        sys.exit()
    except ValueError:
        print(f'{warning} Invalid input! INTEGER 1-10 required.')
        print(f'{warning} Default value implemented!')
        time.sleep(3)
        note_mood = 1
    if note_mood not in range(1,10+1):
        print(f'{warning} Out Of range int detected. Default value implemented!')
        time.sleep(4)
        note_mood = 1 #note mood int
    connection = sqlite3.connect(dbase)
    try:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO notes_DB (date, title, entry, tags, mood, encryptionStatus) VALUES (?, ?, ?, ?, ?, ?)', (date_month_year_time, note_title, note_Entry, note_tag, note_mood, 'NOT-ENCRYPTED'))
    except:
        print('{critic} Critical: Failed to insert data into the database.')
        cursor.close()
        connection.close()
        logger(f"[CRITICAL] Database Error. unable to insert data")
        sys.exit()
    else:
        connection.commit()
        cursor.close()
        connection.close()
        logger(f"[SUCCESSFUL] New note created: '{note_title}'. Entry length: {len(note_Entry)} characters.")
        print(f"{success} Note saved successfully.")
        main_screen()


def main_screen():
    print(f"{info} Loading, Please Wait.")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("[dim]" + "=" * 55 + "[/dim]")
    print("[bold cyan]                CIPHER_NOTE v1.0[/bold cyan]")
    print("[dim]" + "=" * 55 + "[/dim]")

    print(f'''[white]    {date_month_year_time}[white]

    [cyan]Core Commands[/cyan]
    -------------------------------------------------------
    [bold yellow]Command[/bold yellow]        [bold yellow]Description[/bold yellow]
    -------------------------------------------------------
    list           List all notes (ID & title)
    create         Create a new note
    delete         Delete a note by ID
    search         Search for a keyword across notes
    searchtag      Search notes by tag
    viewnote       Display a specific note by ID
    exit           Quit program
    help           Show this help
    clear          Clear the terminal screen
    credits        Show credits and support info
    mood_graph     Display mood analysis chart


    [cyan]Privacy Features[/cyan]
    -------------------------------------------------------
    [bold yellow]Command[/bold yellow]        [bold yellow]Description[/bold yellow]
    -------------------------------------------------------
    logs           View Logs
    lock           Encrypt a specific note ([red]AES-GCM![/red])
    unlock         Decrypt an encrypted note
    lockall        Encrypt all notes ([red]AES-GCM![/red])
    unlockall      Decrypt all encrypted note

    ''')
    Menu()

def Input_Validator(n):
    EXIT = ("q", "exit", "quit", "close", "stop", "end")
    HOME = ('cancel', 'back', 'menu', 'home')
    # attempt to check for exit
    try:
        n = n.lower()
    except:
        pass

    try:
        n = n.strip()
    except: 
        pass

    try:
        n = round(n)
    except:
        pass


    # attempt to fill nagative with "0"
    try:
        if n<0:
            n = 0
    except: pass

    if n in EXIT:
        try:
            cursor.rollback()
            cursor.close()
            connection.close()
        except:
            pass
        print(f"[red]{'='*27} END {'='*27}[/red]\n")
        print(f"[cyan]{fortune.fortune()}[/cyan]\n")
        logger(f"[CRITICAL] Program ended gracefully")
        sys.exit()


    # attempt to check for back command
    elif n in HOME:
        print(f"{warning} Command '{n}' detected. Redirecting to main screen.")
        try:
            cursor.rollback()
            cursor.close()
            connection.close()
        except: 
            pass
        main_screen()

    # else
    else:
        return n

def logger(action):
    # Dog watch in instance a live connection is running =)
    try:
        cursor.close()
        connection.close()
    except: 
        pass

    try:
        connection = sqlite3.connect(dbase)
    except:
        print(f'{warning} Logger failed!, database unable to respond!')
    else:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS logs_DB
                          (date TEXT NOT NULL,
                          action TEXT NOT NULL)''')
        cursor.execute('INSERT INTO logs_DB (date, action) VALUES (?, ?)', (date_month_year_time, action))
        connection.commit()
        cursor.close()
        connection.close()

