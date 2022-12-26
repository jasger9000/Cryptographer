from time import strftime
from tktooltip import ToolTip
from tkinter import HORIZONTAL, UNDERLINE, IntVar, Toplevel, font, messagebox, Tk, Menu, TclError
from ttkbootstrap import Button, Combobox, Notebook, Progressbar, Entry, Radiobutton, Checkbutton, Label, Frame, LabelFrame, Style
from Sym_Cryptographer import Window as SymWindow
from Asym_Cryptographer import Window as AsymWindow
import logging
import requests
from packaging.version import parse
from urllib import request
import os
import zipfile
from subprocess import Popen
from configparser import ConfigParser
import threading
import json
import updater
import sys


version = 'v0.7.0'
stagedConfig = {}
logFile = f'{os.environ["TEMP"]}/Cryptographer Logs/Cryptographer_{version}_{strftime("%d-%m-%Y-%H-%M-%S")}.log'

# logger config
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s', datefmt="%d/%m/%Y %H:%M:%S")

# fileHandler config
if not os.path.exists(f'{os.environ["TEMP"]}/Cryptographer Logs/'):
    os.system('mkdir "%tmp%\Cryptographer Logs"')
fileHandler = logging.FileHandler(logFile)
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(fmt)
logger.addHandler(fileHandler)


# streamHandler config
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(fmt)
streamHandler.setLevel(logging.DEBUG)
logger.addHandler(streamHandler)


def resourcePath(relativePath):
    """Creates a connection to a Ressource like an image which is compiled when the application is freezed to be able to still access it"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relativePath)

def generateConfig():
    """Generates a new config and saves it to config.ini in the installation folder"""
    config = ConfigParser()

    logger.info('Generating new config')
    config.add_section('Settings')
    config.set('Settings', 'Language', 'English')
    config.set('Settings', 'SaveLastKey', '0')
    config.set('Settings', 'Password', 'False')
    config.set('Settings', 'CFUatStartup', '1')
    config.set('Settings', 'Theme', '1')
    config.set('Settings', 'DefaultPath', os.path.expandvars(R'C:\Users\$USERNAME\Documents'))
    
    config.add_section('State')
    config.set('State', 'Mode', 'Symmetric')
    config.set('State', 'Keyfile', 'None')
    config.set('State', 'PublicKeyfile', 'None')
    config.set('State', 'PrivateKeyfile', 'None')
    config.set('State', 'locked', 'False')
    config.set('State', 'Password', 'None')
    config.set('State', 'Version', '1')

    with open('config.ini', 'w') as f:
        config.write(f)
    logger.info('New Config generated')

def LoadConfig():
    """Loads the config from config.ini in memory and generates a new one if it doesn't exist"""
    config = ConfigParser()

    logger.info('Searching for config')
    if os.path.exists('config.ini') is False:
       generateConfig()
       config.read('config.ini')
    else:
        logger.info('Config found, loading now')
        config.read('config.ini')

        if int(config['State']['Version']) < 1:
            logger.warning('Config too old')
            os.remove('config.ini')
            generateConfig()
            config.read('config.ini')
    
    
    lang = LoadLang(config['Settings']['Language'])
    if config['Settings']['theme'] == '1':
        Style('litera')
        logger.info('Using Light theme')
    else:
        Style('darkly')
        logger.info('Using Dark theme')

    logger.info('Config loaded')
    return config, lang


def UpdateConfig(section: str | None, option: str | None, value: str | None, apply: bool = False):
    """Stages and updates the config file in 3 different modes
    ## Mode 1
    In this mode you stage a change to the config but don't apply it until the function gets called in the second mode

    Raises ValueError if the option does not exist in the config in the given section 

    ### Arguments
    section: the section of the config you want to change
    option: the option of the config you want to change
    value: the value you want to be the option
    apply: you can completely ignore this it does not serve a function in the first mode

    ## Mode 2
    In this mode you apply every staged change that was given in the session

    ### Arguments
    section: you can completely ignore this it does not serve a function in the second mode
    option: you can completely ignore this it does not serve a function in the second mode
    value: you can completely ignore this it does not serve a function in the second mode
    apply: THIS NEEDS TO BE True

    ## Mode 3
    In this mode you directly apply a value to an option in the config without staging it first

    Raises ValueError if the option does not exist in the config in the given section

    ### Arguments
    section: the section of the config you want to change
    option: the option of the config you want to change
    value: the value you want to be the option
    apply: THIS NEEDS TO BE True
    """
    global stagedConfig

    # Mode 1
    if apply == False:
        
        # Makes the Apply Button in the Settings Window pressaale if the window is open
        try:
            ApplyBtn['state'] = 'normal'
        except NameError:
            pass

        if config.has_option(section, option):
            if stagedConfig.get(section):
                stagedConfig[section].update({option: value})
            else:
                stagedConfig.update({section: {option: value}})
            logger.info('Staged value change in config')
        else:
            # If the option doesn't exist in the section
            raise ValueError(f'The option "{option}" in the section "{section}" does not exist')
    # Mode 2
    elif apply == True and section is None:
        if stagedConfig > 0:
            for section in stagedConfig.keys():
                for option in stagedConfig[section]:
                    value = stagedConfig[section][option]
                    config.set(section, option, value)
            with open('config.ini', 'w') as f:
                config.write(f)
            stagedConfig.clear()
            logger.info('Applied all staged changes to the config')
        else:
            logger.info('There are no staged changes that could be applied')
    # Mode 3
    elif apply == True and section is not None:
        if config.has_option(section, option):
            config.set(section, option, value)
            with open('config.ini', 'w') as f:
                config.write(f)
            logger.info('Applied value change to config directly')
        else:
            # If the option doesn't exist in the section
            raise ValueError(f'The option "{option}" in the section "{section}" does not exist')


def CheckForUpdates(automatic: bool = True, pVersion: str = None):
    """Checks for updates of the software and gives the user an installation prompt if an update was found
    If the automatic parameter is False it additionally gives the user a prompt for when there was no update or no connection to the server
    If pVersion is provided, it is given as a means to check for updates instead of the version variable"""
    if isinstance(pVersion, str):
        version = pVersion

    new_update = updater.CheckNewVersion(version, 'https://github.com/jasger9000/Cryptographer/')

    if isinstance(new_update, str): # Gets triggered if a new update is available
        if messagebox.askyesno(getTranslation('UpdateAvailableTrue', 'Title'), getTranslation('UpdateAvailableTrue', 'Message')):
            InstallNewUpdate(new_update)
    elif new_update is False and automatic is False: # Gets triggered if no update is available and the user requested to check for updates
        messagebox.showinfo(getTranslation('UpdateAvailableFalse', 'Title'), getTranslation('UpdateAvailableFalse', 'Message'))
    elif new_update is None and automatic is False: # gets triggered if a connection to the server was not possible and the user requested to check for updates
        messagebox.showerror(getTranslation('UpdateConnectionError', 'Title'),getTranslation('UpdateConnectionError', 'Message'))

def InstallNewUpdate(latest: str):
    """Installs the new Update that was downloaded"""

    # Create an Install window
    InstallWindow = Toplevel(root)
    InstallWindow.title(getTranslation('window', 'installWindowTitle'))
    InstallWindow.iconbitmap(resourcePath('UI/download.ico'))
    InstallWindow.resizable(0, 0)
    InstallWindow.focus()
    InstallWindow.transient(root)
    InstallWindow.grab_set()
    logger.info('Loaded UpdateWindow Window config')

    Label(InstallWindow, text=getTranslation('window', 'installWindowTitle'), font=('Helvetica', 14, font.BOLD, UNDERLINE)).grid(row=0, column=0, pady=12)

    # creates widgets for window
    finishable = False
    InstallBar = Progressbar(InstallWindow, orient=HORIZONTAL, length=200, mode='indeterminate')
    InstallBar.grid(row=1, column=0, ipady=8.499999999999999115)
    FinishBtn = Button(InstallWindow, text='Finish', command=finishable is True, state='disabled')
    InstallBar.start()

    # downloads an install the new version
    if updater.DownloadVersion(latest, "https://github.com/jasger9000/Cryptographer/", "Cryptographer.zip", os.getcwd(), ["UI", "Languages/English.py"]):
        FinishBtn['state'] = 'normal'
        InstallBar['value'] = 100
        InstallBar.stop()

        # waits until user clicks finish Button then closes the application and opens the new one
        while finishable is not True:
            Popen(f'cd /d {os.getcwd()} && start python -c "from updater import InstallVersion; InstallVersion({chr(39)}{os.getcwd()}{chr(39)}, {chr(39)}Cryptographer.zip{chr(39)}, {chr(39)}Cryptographer.exe{chr(39)}, True)" && exit', shell=True)
            root.destroy()

        if mode == 'Symmetric':      
            SymWindow(EncryptFrame, DecryptFrame, KeyFrame, out)
            KeyFrame.config(text=lang.Main['KeyTitle'])
            root.title(f'{lang.Main["title"]} {version}')
            TitleLabel.config(text=lang.Main["title"])
            UpdateConfig('State', 'Mode', 'Symmetric', True)
        elif mode == 'Asymmetric':
            AsymWindow(EncryptFrame, DecryptFrame, KeyFrame, out, lang.Language)
            KeyFrame.config(text=lang.AsymMain['KeysTitle'])
            root.title(f'{lang.AsymMain["title"]} {version}')
            TitleLabel.config(text=lang.AsymMain["title"])
            UpdateConfig('State', 'Mode', 'Asymmetric', True)
        logger.info('Loading complete')

def LoadFrames():
    global EncryptFrame, DecryptFrame, KeyFrame

    # Tabs
    TabRegister = Notebook(root)
    TabRegister.grid(row=1, column=0, padx=20)

    EncryptFrame = Frame(TabRegister)
    DecryptFrame = Frame(TabRegister)

    EncryptFrame.pack(fill='both', expand=1)
    DecryptFrame.pack(fill='both', expand=1)

    TabRegister.add(EncryptFrame, text=lang.Dialog['Encrypt'])
    TabRegister.add(DecryptFrame, text=lang.Dialog['Decrypt'])

def LoadLang(l):
    """Loads a Language pack if it is installed and asks the user to reinstall the English one if the users and the English one is missing.
    Returns the language pack if it is installed otherwise returns None"""
    if os.path.exists('Languages'):
        logger.info('Loading Language')

        if os.path.exists(f'Languages/{l}.json'): # Checks if Language pack exists and loads it if it does
            with open(f'Languages/{l}.json', 'r') as f:
                lang = json.load(f)
            logger.info('Loaded ' + l + ' Language pack')
        elif os.path.exists('Languages/English.json'): # Checks if English Language pack is installed to try to fallback
            logger.error('Language not found, continuing with English')
            messagebox.showerror("Language not found", "Couldn't find the Language you are trying to use, please reinstall the Language pack")
            with open('Languages/English.json', 'r') as f:
                lang = json.load(f)
            UpdateConfig('Settings', 'Language', "English")
        else: # Asks the user to reinstall the English Language pack
            logger.exception('English Language pack not installed')
            messagebox.showerror('English not found', 'Cryptographer tried to fallback to English but failed because English is not installed.\nPlease reinstall the English Language pack.')
            if messagebox.askyesno('Reinstall English', 'Reinstall English Language pack?'):
                try:
                    logger.info('Trying to reinstall English')
                    request.urlretrieve('https://raw.githubusercontent.com/jasger9000/Cryptographer/master/Languages/English.json', 'Languages/English.json')
                    UpdateConfig('Settings', 'Language', "English")
                except error.URLError:
                    logger.error('Connection to server could not be established')
                    messagebox.showerror("Couldn't reinstall English", "Couldn't reinstall English because connection to GitHub couldn't be Established.\nPlease try again later or check if you are Connected to the Internet.")
                    return None
            else:
                logger.info('User did not try to reinstall the English language pack, exiting application')
                return None
        return lang
    else:
        logger.error('Language folder not found, creating new')
        os.mkdir('Languages')
        LoadLang(None)

def getTranslation(groupKey: str, itemKey: str):
    """Gets a translation for a given key from the language pack"""
    global lang

    try:
        return lang[groupKey][itemKey]
    except TypeError:
        logger.exception('Language key was referenced before Language pack was loaded')
        messagebox.showerror('Language key referenced before Language was loaded', 
        f'''It was tried to load a language key before the Language pack was loaded, it should not be possible to receive this error.
        Please open an issue and attach the log file of your current session.
        GitHub: https://github.com/jasger9000/Cryptographer
        Log file: {logFile}''')
        root.destroy()
    except KeyError:
        logger.exception('The Key entered does not exist in this Language pack')

    Label(InstallWindow, text=lang.CryptMain['InstallUpdateTitle']).grid(row=0, column=0, pady=6, padx=10)
    InstallBar = Progressbar(InstallWindow, orient=HORIZONTAL, length=200, mode='determinate')
    InstallBar.grid(row=1, column=0, ipady=8.499999999999999115)
    FinishBtn = Button(InstallWindow, text='Finish', command=lambda: [logger.info('Finished installing, restarting now'), Popen(f'"{os.getcwd()}/Cryptographer {latest}.exe"'), root.destroy()], state='disabled')
    FinishBtn.grid(row=1, column=1)
    ProgressLabel = Label(InstallWindow, text='')
    ProgressLabel.grid(row=2, column=0, pady=10)
    
    logger.info('Downloading Update')
    ProgressLabel.config(text=lang.CryptMain['InstallUpdateProgress0'])
    file = f'{os.getcwd()}/Cryptographer.zip'
    url = f'https://github.com/jasger9000/Cryptographer/releases/download/{latest}/Cryptographer.zip'
    request.urlretrieve(url, file)
    InstallBar['value'] += 66
    logger.info('Update downloaded')

    ProgressLabel.config(text=lang.CryptMain['InstallUpdateProgress1'])
    os.system('rmdir UI /S /Q')
    os.remove('Languages/English.py')
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())
    InstallBar['value'] += 66
    logger.info('Extracted Update')

    ProgressLabel.config(text=lang.CryptMain['InstallUpdateProgress2'])    
    if os.path.exists(file):
        os.remove(file)
    InstallBar['value'] += 67
    ProgressLabel.config(text=lang.CryptMain['InstallUpdateProgress3'])
    FinishBtn['state'] = 'normal'

def Copy():
    logger.info('Copy function initiated')
    try:
        root.clipboard_clear()
        root.clipboard_append(out.get())
    except Exception:
        messagebox.showerror(title=getTranslation('unknownError', 'Title'), message=getTranslation('unknownError', 'Message'))
        logger.exception(f'Unknown error/uncaught exception in Copy function')
    finally:
        logger.info('Copy function finished')

def Delete():
    logger.info('Delete function initiated')
    try:
        out.config(state='normal')
        out.delete(0, 'end')
    except Exception:
        messagebox.showerror(title=getTranslation('unknownError', 'Title'), message=getTranslation('unknownError', 'Message'))
        logger.exception(f'Unknown/uncaught exception in Delete function')
    finally:
        out.config(state='readonly')
        logger.info('Delete function finished')


    SettingsWindow.title(getTranslation('window', 'settingsWindowTitle'))
    Label(SettingsWindow, text=getTranslation('window', 'settingsWindowTitle') , font=('Helvetica', 14, font.BOLD, UNDERLINE)).grid(row=0, column=0, pady=12)
    Label(SettingsFrame, text=getTranslation('SettingsMenu', 'general'), font=('Helvetica', 8, font.BOLD, UNDERLINE)).grid(row=0, column=0, pady=(12, 2))
    Label(SettingsFrame, text=getTranslation('SettingsMenu', 'languageOptionLabel')).grid(row=1, column=0, pady=5)
    Button(SettingsFrame, text=getTranslation('SettingsMenu', 'addNewLanguageBtn'), command=InstallNewLanguage).grid(row=1, column=2, pady=5)
    SaveLabel = Label(SettingsFrame, text=getTranslation('SettingsMenu', 'rememberKeyOptionLabel'))
    ToolTip(SaveLabel, msg=getTranslation('SettingsMenu', 'rememberKeyOptionTip'))
    Label(SettingsFrame, text=getTranslation('SettingsMenu', 'autoCFUOptionLabel')).grid(row=3, column=0, pady=5, padx=(0, 20))
    Label(SettingsFrame, text=getTranslation('SettingsMenu', 'themes'), font=('Helvetica', 8, font.BOLD, UNDERLINE)).grid(row=4, column=0, pady=(12, 2))
    Label(SettingsFrame, text=getTranslation('SettingsMenu', 'lightTheme')).grid(row=5, pady=5)
    Label(SettingsFrame, text=getTranslation('SettingsMenu', 'darkTheme')).grid(row=6, pady=5)
    DefaultBtn = Button(frame, text=getTranslation('SettingsMenu', 'defaultBtn'), command=lambda: [generateConfig(), root.destroy(), os.startfile(f'{os.getcwd()}/Cryptographer.exe')])
    ApplyBtn = Button(frame, state='disabled',text=getTranslation('SettingsMenu', 'applyBtn'), command=lambda: UpdateConfig(apply=True))
        root.title(f'{getTranslation("window", "symTitle")} {version}')
        TitleLabel.config(text=getTranslation('window', 'symTitle'))
        root.title(f'{getTranslation("window", "asymTitle")} {version}')
        TitleLabel.config(text=getTranslation('window', 'asymTitle'))
def main():
    global root, TitleLabel, out, lang, config

    # Tk Config
    root = Tk()
    root.resizable(0,0)
    root.geometry('300x300')
    TitleLabel = Label(root, text='', font=('Helvetica', 14, font.BOLD, UNDERLINE)) # text will change when loading a mode
    TitleLabel.grid(row=0, column=0, columnspan=2, pady=12)
    updater.addFileHandlerLogging(logFile)
    config, lang = LoadConfig()
    if not lang:
        return
        
    try:
        root.title(f'Cryptographer {version}')
        root.iconbitmap('Cryptographer.exe')
    except TclError:
        logger.warning("Couldn't find icon, continuing without")
    except NameError:
        logger.error("Could not find Version variable, corruption likely")
        root.title(getTranslation('versionNotFound', 'Title'))
        root.bell()
        userConfirm = messagebox.askokcancel(lang.VersionNotFound['Title'], lang.VersionNotFound['Message'])
        if messagebox.askokcancel(getTranslation('versionNotFound', 'Title'), getTranslation('versionNotFound', 'Message')):
            InstallNewUpdate(requests.get('https://api.github.com/repos/jasger9000/Cryptographer/releases/latest').json()['tag_name'])
        else:
            return

    if os.path.exists(f'{os.getcwd()}\Cryptographer {version}.exe'):
        try:
            os.remove(f'{os.getcwd()}\Cryptographer.exe')
        except FileNotFoundError:
            pass
        os.rename(f'{os.getcwd()}\Cryptographer {version}.exe', 'Cryptographer.exe')
        Popen(f'"{os.getcwd()}/Cryptographer.exe"')
        return


    menubar = Menu(root)
    ModeMenu = Menu(menubar, tearoff=0)
    
    # Mode Menu
    ModeMenu.add_command(label=getTranslation('menuBar', 'symLabel'), command=lambda: SwitchMode('Symmetric'))
    ModeMenu.add_command(label=getTranslation('menuBar', 'asymLabel'), command=lambda: SwitchMode('Asymmetric'))
    menubar.add_cascade(label=getTranslation('menuBar', 'mode'), menu=ModeMenu)

    # # History Menu
    # HistoryMenu = Menu(menubar, tearoff=0)
    # menubar.add_cascade(label=getTranslation('menuBar', 'history'), menu=HistoryMenu)
    
    # Help Menu
    HelpMenu = Menu(menubar, tearoff=0)
    HelpMenu.add_command(label=getTranslation('menuBar', 'openGitHub'), command=lambda: Popen('explorer "https://github.com/jasger9000/Cryptographer"'))
    HelpMenu.add_command(label=getTranslation('menuBar', 'openInstallPath'), command=lambda: Popen(f'explorer "{os.getcwd()}"'))
    HelpMenu.add_separator()
    HelpMenu.add_command(label=getTranslation('menuBar', 'settings'), command=OpenSettings)
    HelpMenu.add_separator()
    # HelpMenu.add_command(label=lang.CryptMain['HelpAboutLabel'])
    HelpMenu.add_command(label=getTranslation('menuBar', 'CheckForUpdates'), command=lambda: CheckForUpdates(False))
    menubar.add_cascade(label=getTranslation('menuBar', 'help'), menu=HelpMenu)

    root.config(menu=menubar)

    # Output
    frame3 = LabelFrame(root, text=getTranslation('window', 'outputTitle'))
    frame3.grid(row=2, column=0, padx=10, pady=12, columnspan=2)

    out = Entry(frame3, width=50, state='readonly')
    out.grid(row=0, column=0, padx=5, rowspan=2)
    Button(frame3, text=getTranslation('window', 'copyBtn'), command=Copy).grid(row=0, column=1, padx=10)
    Button(frame3, text=getTranslation('window', 'deleteBtn'), command=Delete).grid(row=1, column=1, padx=10, pady=6)

    if config['Settings']['CFUatStartup'] == '1':
        threading.Thread(target=CheckForUpdates, daemon=True).start()
    if config['State']['Mode'] == 'Symmetric':
        SwitchMode('Symmetric')
    elif config['State']['Mode'] == 'Asymmetric':
        SwitchMode('Asymmetric')
    
    root.mainloop()

if __name__ == '__main__':
    main()