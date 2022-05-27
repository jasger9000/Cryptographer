import importlib
import Asym_Cryptographer
import Sym_Cryptographer
from tkinter import HORIZONTAL, Button, Checkbutton, IntVar, Label, Toplevel, messagebox, Tk, Menu, TclError, ttk
import logging
import requests
from packaging.version import parse
import webbrowser
from urllib import request
import os
import zipfile
import subprocess
from configparser import ConfigParser
import threading
import sys

sys.path.insert(0, 'Languages')

# logger config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fmt = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')

# fileHandler config
fileHandler = logging.FileHandler('Cryptographer.log')
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(fmt)
logger.addHandler(fileHandler)
with open('Cryptographer.log', 'w') as f:
    f.write('')

# streamHandler config
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(fmt)
streamHandler.setLevel(logging.DEBUG)
logger.addHandler(streamHandler)

version = '0.6.0'

def OpenSettings():
    global langBox

    # Window Config
    Settings = Toplevel(root, bg='#202124')
    Settings.title(lang.CryptMain['HelpSettingsLabel'])
    Settings.resizable(0,0)
    Settings.focus()
    Settings.transient(root)
    Settings.grab_set()
    Settings.geometry('800x800')

    # Language Setting
    Label(Settings, text=lang.SettingsLabels['LangLabel'], fg="#e8eaed", bg='#202124').grid(row=0, column=0, padx=10, pady=12)
    langList = ['Deutsch', 'English', 'Français'] # PLACEHOLDER
    langBox = ttk.Combobox(Settings, values=langList, state='readonly')
    langBox.set(lang.Language)
    langBox.bind('<<ComboboxSelected>>', LoadLang)
    langBox.grid(row=0, column=1)
    Button(Settings, text=lang.SettingsLabels['AddLangBtn'], command=InstallNewLanguage)

    # Save key?
    Label(Settings, text=lang.SettingsLabels['RememberKeyLabel'], background='#202124', foreground='#e8eaed').grid(row=1, column=0)
    saveKey = IntVar()
    saveKey.set(config['Settings']['SaveLastKey'])
    Checkbutton(Settings, variable=saveKey, onvalue=1, offvalue=0, command=lambda: UpdateConfig('Settings', 'SaveLastKey', str(saveKey.get())), background='#202124').grid(row=1, column=1) # Also need to save State

    # Automatic CFU?
    Label(Settings, text=lang.SettingsLabels['AutoCFULabel'], background='#202124', foreground='#e8eaed').grid(row=2, column=0)
    autoCFU = IntVar()
    autoCFU.set(config['Settings']['CFUatStartup'])
    Checkbutton(Settings, variable=autoCFU, onvalue=1, offvalue=0, command=lambda: UpdateConfig('Settings', 'CFUatStartup', str(autoCFU.get())), background='#202124').grid(row=2, column=1)

    Button(Settings, text=lang.SettingsLabels['ApplyBtn'], command=lambda: [root.destroy(), main()]).grid(row=15, column=1)
    root.wait_window()


def InstallNewLanguage():
    requests.get('https://api.github.com/repos/jasger9000/Cryptographer/releases/latest').json()['tag_name']    


    

def switchSymmetric():
    global frameA0, frameA1, frameA2, frameA3, TitleLabelA
    
    if loaded is True and config['State']['Mode'] == 'Asymmetric':
        Asym_Cryptographer.Unload(frameB0, frameB1, frameB2, frameB3, TitleLabelB)

    if loaded is False or config['State']['Mode'] != 'Symmetric':      
        logger.info('Loading Symmetric Cryptographer')
        frameA0, frameA1, frameA2, frameA3, TitleLabelA = Sym_Cryptographer.main(root, version, lang.Language)
        UpdateConfig('State', 'Mode', 'Symmetric')
        logger.info('Loading complete')

def switchAsymmetric():
    global frameB0, frameB1, frameB2, frameB3, TitleLabelB
    
    if loaded is True and config['State']['Mode'] == 'Symmetric':
        Sym_Cryptographer.Unload(frameA0, frameA1, frameA2, frameA3, TitleLabelA)

    if loaded is False or config['State']['Mode'] != 'Asymmetric':   
        logger.info('Loading Asymmetric Cryptographer')
        frameB0, frameB1, frameB2, frameB3, TitleLabelB = Asym_Cryptographer.main(root ,version, lang.Language)
        UpdateConfig('State', 'Mode', 'Asymmetric')
        logger.info('Loading complete')


def CheckForUpdates(mode: str):
    global lang
    try:
        logger.info('Trying to get latest version')
        latest = requests.get('https://api.github.com/repos/jasger9000/Cryptographer/releases/latest').json()['tag_name']
        logger.info('Got latest version')
        if parse(latest) > parse(version):
            logger.info('Newer Version found')
            newUpdate = True
        else:
            logger.info('No new version found')
            newUpdate = False
    except Exception:
        logger.warning("Couldn't connect to server")
        newUpdate = latest = None

    if newUpdate:
        userConfirm = messagebox.askyesno(lang.NewUpdateTrue['Title'], lang.NewUpdateTrue['Message'])
        if userConfirm:
            InstallNewUpdate(latest)
    elif latest is None and mode == 'manual':
        messagebox.showerror(lang.NewUpdateFalse['Title1'], lang.NewUpdateFalse['Message1'])
    elif mode == 'manual':
        messagebox.showinfo(lang.NewUpdateFalse['Title2'], lang.NewUpdateFalse['Message2'])

def InstallNewUpdate(latest: str):
    InstallWindow = Toplevel()
    InstallBar = ttk.Progressbar(InstallWindow, orient=HORIZONTAL, length=100, mode='determinate')
    InstallBar.grid(row=0, column=0, pady=20)
    logger.info('Downloading Update')
    file = f'{os.getcwd()}/Cryptographer.zip'
    url = f'https://github.com/jasger9000/Cryptographer/releases/download/{latest}/Cryptographer.zip'
    request.urlretrieve(url, file)
    logger.info('Update downloaded')

    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())
    logger.info('Extracted Update')

    if os.path.exists(file):
        os.remove(file)
    logger.info('Finished installing, restarting now')
    subprocess.Popen(f'"{os.getcwd()}/Cryptographer {latest}.exe"')
    root.destroy()


def main():
    global root, loaded
    loaded = False

    if os.path.basename(os.getcwd()) == f'Cryptographer {version}':
        os.rename(os.path.basename(os.getcwd()), 'Cryptographer.py')

    # Tk Config
    root = Tk()
    root.resizable(0,0)
    root.geometry('300x300')
    LoadConfig()
    try:
        root.title(f'Cryptographer ver. {version}')
        root.iconbitmap('Cryptographer.exe')
    except TclError:
        logger.warning("Couldn't find icon, continuing without")
    except NameError:
        logger.error("Could not find Version variable, corruption likely")
        root.title(lang.VersionNotFound['Title'])
        root.bell()
        userConfirm = messagebox.askokcancel(lang.VersionNotFound['Title'], lang.VersionNotFound['Message'])
        if userConfirm:
            InstallNewUpdate(requests.get('https://api.github.com/repos/jasger9000/Cryptographer/releases/latest').json()['tag_name'])
        else:
            root.destroy()
    if config['State']['Mode'] == 'Symmetric':
        switchSymmetric()
    elif config['State']['Mode'] == 'Asymmetric':
        switchAsymmetric()

    menubar = Menu(root)
    ModeMenu = Menu(menubar, tearoff=0)
    
    # Mode Menu
    ModeMenu.add_command(label=lang.CryptMain['ModeSymLabel'], command=switchSymmetric)
    ModeMenu.add_command(label=lang.CryptMain['ModeAsymLabel'], command=switchAsymmetric)
    menubar.add_cascade(label=lang.CryptMain['ModeMenu'], menu=ModeMenu)

    # History Menu
    HistoryMenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label=lang.CryptMain['HistoryMenu'], menu=HistoryMenu)
    
    # Help Menu
    HelpMenu = Menu(menubar, tearoff=0)
    HelpMenu.add_command(label=lang.CryptMain['HelpGithubLabel'], command=lambda: webbrowser.open('https://github.com/jasger9000/Cryptographer'))
    HelpMenu.add_command(label=lang.CryptMain['HelpFilesLabel'], command=lambda: subprocess.Popen(f'explorer "{os.getcwd()}"'))
    HelpMenu.add_separator()
    HelpMenu.add_command(label=lang.CryptMain['HelpSettingsLabel'], command=OpenSettings)
    HelpMenu.add_separator()
    HelpMenu.add_command(label=lang.CryptMain['HelpAboutLabel'])
    HelpMenu.add_command(label=lang.CryptMain['HelpCFULabel'], command=lambda: CheckForUpdates('manual'))
    menubar.add_cascade(label=lang.CryptMain['HelpMenu'], menu=HelpMenu)

    root.config(menu=menubar)
    
    if config['Settings']['CFUatStartup'] == '1':
        threading.Thread(target=lambda: CheckForUpdates('automatic')).start()

    loaded = True
    root.mainloop()


def LoadLang(l: str):
    if type(l) is not str:
        l = langBox.get()
    try:
        lang = importlib.import_module(l)
        UpdateConfig('Settings', 'Language', l)
    except ModuleNotFoundError:
        logger.error('Language Module not found, continuing with English')
        messagebox.showerror("Language not found", "Couldn't find the Language you are trying to use, please reinstall the Language pack")
        UpdateConfig('Settings', 'Language', 'English')
        lang = importlib.import_module('English')
        logger.exception('Language Module not found, continuing with English')
    except NameError: # Triggers when config is not defined e.g. when lang is imported in sym or Asym
        pass
    return lang


def LoadConfig():
    global config, lang
    config = ConfigParser()

    logger.info('Searching for config')
    if os.path.exists('config.ini'):
        logger.info('Config found, loading...')
        config.read('config.ini')

        lang = LoadLang(config['Settings']['Language'])
        logger.info('Config loaded')
    else:
        logger.warning('Config not found, generating new')
        config.add_section('Settings')
        config.set('Settings', 'Language', 'English')
        config.set('Settings', 'SaveLastKey', '0')
        config.set('Settings', 'Password', 'False')
        config.set('Settings', 'CFUatStartup', '1')
        config.set('Settings', 'Mode', 'Light')
        config.set('Settings', 'DefaultPath', os.path.expandvars(R'C:\Users\$USERNAME\Documents'))
        
        config.add_section('State')
        config.set('State', 'Mode', 'None')
        config.set('State', 'Keyfile', 'None')
        config.set('State', 'PublicKeyfile', 'None')
        config.set('State', 'PrivateKeyfile', 'None')
        config.set('State', 'locked', 'False')
        config.set('State', 'Password', 'None')
        with open('config.ini', 'w') as f:
            config.write(f)
        lang = LoadLang('English')
        logger.info('New Config generated')
    return config

def LoadFilesTypes(lang):
    return (
        (lang.fileTypes['Text'], ('*.txt', '*.doc', '*.docx', '*.log', '*.msg', '*.odt', '*.pages', '*.rtf', '*.tex', '*.wpd', '*.wps')),                   # 0
        (lang.fileTypes['Video'], ('*.mp4', '*.mov', '*.avi', '*.flv', '*.mkv', '*.wmv', '*.avchd', '*.webm', '*MPEG-4', '*.H.264')),                       # 1
        (lang.fileTypes['Audio'], ('*.aif', '*.aiff', '*.iff', '*.m3u', '*.m4a', '*.mp3', '*.mpa', '*.wav', '*.wma', '*.aup3', '*.aup', '*.ogg', '*.mp2')), # 2
        (lang.fileTypes['Picture'], ('*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp', '*.raw', '*.tiff', '*.psd', '*.cr2')),                                   # 3
        (lang.fileTypes['All'], '*.*'),                                                                                                                     # 4
        (lang.fileTypes['Encrypted'], '*.Encrypted'),                                                                                                       # 5
        (lang.fileTypes['Key'], '*.key'),                                                                                                                   # 6
        (lang.fileTypes['PrivateKey'], '*.priv_key'),                                                                                                       # 7
        (lang.fileTypes['PublicKey'], '*.pub_key'),                                                                                                         # 8
        )


def UpdateConfig(Section: str, Option: str, Value: str):
    config.set(Section, Option, Value)
    with open('config.ini', 'w') as f:
            config.write(f)


if __name__ == '__main__':
    # TODO Make apply Btn only appear after changes
    # TODO Keyfile
    # TODO PublicKeyfile
    # TODO PrivateKeyfile
    # TODO locked
    # TODO Password
    # TODO Make VersionNotFound Window always focused
    # TODO Make installation Progress Bar
    # TODO History
    # TODO Light/dark mode
    # TODO DefaultPath
    main()