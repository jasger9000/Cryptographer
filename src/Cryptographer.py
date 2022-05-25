import importlib
import Asym_Cryptographer
import Sym_Cryptographer
from tkinter import Button, Checkbutton, IntVar, Label, StringVar, Toplevel, messagebox, Tk, Menu, TclError, ttk
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
    Settings.geometry('300x300')

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
    Checkbutton(Settings, variable=saveKey, onvalue=True, offvalue=False, command=lambda: UpdateConfig(), background='#202124').grid(row=1, column=1) # Also need to save State

    Button(Settings, text=lang.SettingsLabels['ApplyBtn'], command=lambda: [root.destroy(), main()]).grid(row=2, column=1)
    root.wait_window()


def InstallNewLanguage():
    requests.get('https://api.github.com/repos/jasger9000/Cryptographer/releases/latest').json()['tag_name']    


    

def switchSymmetric():
    global frameA0, frameA1, frameA2, frameA3, TitleLabelA
    
    if loaded is True and config['State']['Mode'] != 'Symmetric':
        Asym_Cryptographer.Unload(frameB0, frameB1, frameB2, frameB3, TitleLabelB)

    if loaded is False or config['State']['Mode'] != 'Symmetric':      
        logger.info('Loading Symmetric Cryptographer')
        frameA0, frameA1, frameA2, frameA3, TitleLabelA = Sym_Cryptographer.main(root, version)
        UpdateConfig('State', 'Mode', 'Symmetric')
        logger.info('Loading complete')

def switchAsymmetric():
    global frameB0, frameB1, frameB2, frameB3, TitleLabelB
    
    if loaded is True and config['State']['Mode'] != 'Asymmetric':
        Sym_Cryptographer.Unload(frameA0, frameA1, frameA2, frameA3, TitleLabelA)

    if loaded is False or config['State']['Mode'] != 'Asymmetric':   
        logger.info('Loading Asymmetric Cryptographer')
        frameB0, frameB1, frameB2, frameB3, TitleLabelB = Asym_Cryptographer.main(root ,version)
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
    subprocess.Popen(f'"{os.getcwd()}/Cryptographer.exe"')
    root.destroy()


def main():
    global root, loaded
    loaded = False

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
        userConfirm = messagebox.askokcancel(lang.VersionNotFound['Title'], lang.VersionNotFound['Message'])
        root.bell()
        if userConfirm:
            InstallNewUpdate(requests.get('https://api.github.com/repos/jasger9000/Cryptographer/releases/latest').json()['tag_name'])
        else:
            root.destroy()

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
    
    if config['Settings']['CFU at startup']:
        threading.Thread(target=lambda: CheckForUpdates('automatic')).start()

    loaded = True
    root.mainloop()



def LoadLang(l: str):
    global lang
    
    if type(l) is not str:
        l = langBox.get()
    try:
        lang = importlib.import_module(f'Languages.{l}')
        UpdateConfig('Settings', 'Language', l)
    except ModuleNotFoundError:
        logger.error('Language Module not found, continuing with English')
        messagebox.showerror("Language not found", "Couldn't find the Language you are trying to use, please reinstall the Language pack")
        UpdateConfig('Settings', 'Language', 'English')
        lang = importlib.import_module(f'Languages.English')
    except NameError:
        pass

def LoadConfig():
    global config
    config = ConfigParser()

    logger.info('Searching for config')
    if os.path.exists('config.ini'):
        logger.info('Config found, loading...')
        config.read('config.ini')

        LoadLang(config['Settings']['Language'])
        if config['State']['Mode'] == 'Symmetric':
            switchSymmetric()
        elif config['State']['Mode'] == 'Asymmetric':
            switchAsymmetric()
        logger.info('Config loaded')
    else:
        logger.warning('Config not found, generating new')
        config.add_section('Settings')
        config.set('Settings', 'Language', 'English')
        config.set('Settings', 'Save Last Key', 'False')
        config.set('Settings', 'Password', 'False')
        config.set('Settings', 'CFU at startup', 'True')
        config.set('Settings', 'Mode', 'Light')
        config.set('Settings', 'Default Path', os.path.expandvars(R'C:\Users\$USERNAME\Documents'))
        
        config.add_section('State')
        config.set('State', 'Mode', 'None')
        config.set('State', 'Keyfile', 'None')
        config.set('State', 'Public Keyfile', 'None')
        config.set('State', 'Private Keyfile', 'None')
        config.set('State', 'locked', 'False')
        config.set('State', 'Password', 'None')
        with open('config.ini', 'w') as f:
            config.write(f)
        LoadLang('English')
        logger.info('New Config generated')
    return config

def UpdateConfig(Section: str, Option: str, Value: str):
    config.set(Section, Option, Value)
    with open('config.ini', 'w') as f:
            config.write(f)


if __name__ == '__main__':
    # TODO Keyfile
    # TODO Public Keyfile
    # TODO Private Keyfile
    # TODO locked
    # TODO Password
    # TODO Make VersionNotFound Window always focused
    # TODO Make installation Progress Bar
    main()