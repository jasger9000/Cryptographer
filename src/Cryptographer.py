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

def UpdateConfig(Section: str, Option: str | list, Value: str, Apply=False):
    global stagedConfig

    try:
        ApplyBtn['state'] = 'normal'
    except NameError:
        pass
    
    if type(Option) is list:
        if Apply == True:
            for i in Option:
                config.set(Section, i, Value)
                with open('config.ini', 'w') as f:
                    config.write(f)
        else:
            [stagedConfig.update({i: [Section, Value]}) for i in Option if i]
    else:
        if Apply == True:
            config.set(Section, Option, Value)
            with open('config.ini', 'w') as f:
                config.write(f)
        else:
            stagedConfig.update({Option: [Section, Value]})


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

    # Keyframe
    KeyFrame = LabelFrame(root, text='')
    KeyFrame.grid(row=1, column=1, padx=10)

def CheckForUpdates(mode: str):
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
    except ConnectionError:
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
    InstallWindow = Toplevel(root, padx=10)
    InstallWindow.iconbitmap(resource_path('UI/download.ico'))
    InstallWindow.resizable(0,0)
    InstallWindow.focus()
    InstallWindow.transient(root)
    InstallWindow.grab_set()

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
        messagebox.showerror(title=lang.Messages['UnknownTitle'], message=lang.Messages['UnknownMessage'])
        logger.exception(f'Unknown error/uncaught exception in Copy function')
    finally:
        logger.info('Copy function finished')

def Delete():
    logger.info('Delete function initiated')
    try:
        out.config(state='normal')
        out.delete(0, 'end')
    except Exception:
        messagebox.showerror(title=lang.Messages['UnknownTitle'], message=lang.Messages['UnknownMessage'])
        logger.exception(f'Unknown/uncaught exception in Delete function')
    finally:
        out.config(state='readonly')
        logger.info('Delete function finished')


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
        root.title(lang.VersionNotFound['Title'])
        root.bell()
        userConfirm = messagebox.askokcancel(lang.VersionNotFound['Title'], lang.VersionNotFound['Message'])
        if userConfirm:
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
    ModeMenu.add_command(label=lang.CryptMain['ModeSymLabel'], command=lambda: SwitchMode('Symmetric'))
    ModeMenu.add_command(label=lang.CryptMain['ModeAsymLabel'], command=lambda: SwitchMode('Asymmetric'))
    menubar.add_cascade(label=lang.CryptMain['ModeMenu'], menu=ModeMenu)

    # # History Menu
    # HistoryMenu = Menu(menubar, tearoff=0)
    # menubar.add_cascade(label=lang.CryptMain['HistoryMenu'], menu=HistoryMenu)
    
    # Help Menu
    HelpMenu = Menu(menubar, tearoff=0)
    HelpMenu.add_command(label=lang.CryptMain['HelpGithubLabel'], command=lambda: Popen('explorer "https://github.com/jasger9000/Cryptographer"'))
    HelpMenu.add_command(label=lang.CryptMain['HelpFilesLabel'], command=lambda: Popen(f'explorer "{os.getcwd()}"'))
    HelpMenu.add_separator()
    HelpMenu.add_command(label=lang.CryptMain['HelpSettingsLabel'], command=OpenSettings)
    HelpMenu.add_separator()
    # HelpMenu.add_command(label=lang.CryptMain['HelpAboutLabel'])
    HelpMenu.add_command(label=lang.CryptMain['HelpCFULabel'], command=lambda: CheckForUpdates('manual'))
    menubar.add_cascade(label=lang.CryptMain['HelpMenu'], menu=HelpMenu)

    root.config(menu=menubar)

    # Output
    frame3 = LabelFrame(root, text=lang.Main['OutputTitle'])
    frame3.grid(row=2, column=0, padx=10, pady=12, columnspan=2)

    out = Entry(frame3, width=50, state='readonly')
    out.grid(row=0, column=0, padx=5, rowspan=2)
    Button(frame3, text=lang.Main['CopyBtn'], command=Copy).grid(row=0, column=1, padx=10)
    Button(frame3, text=lang.Main['DeleteBtn'], command=Delete).grid(row=1, column=1, padx=10, pady=6)



    if config['Settings']['CFUatStartup'] == '1':
        threading.Thread(target=CheckForUpdates, daemon=True).start()
    if config['State']['Mode'] == 'Symmetric':
        SwitchMode('Symmetric')
    elif config['State']['Mode'] == 'Asymmetric':
        SwitchMode('Asymmetric')
    
    root.mainloop()

if __name__ == '__main__':
    main()