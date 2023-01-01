from time import strftime
from tktooltip import ToolTip
from tkinter import HORIZONTAL, UNDERLINE, IntVar, Toplevel, font, messagebox, Tk, Menu, TclError
from ttkbootstrap import Button, Combobox, Notebook, Progressbar, Entry, Radiobutton, Checkbutton, Frame, Label, LabelFrame, Style
from PIL import ImageTk, Image
import logging
import os
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
    """Creates a connection to a Ressource like an image which is compiled when the application is frozen to be able to still access it"""
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
    """Stages and updates the config file in 2 different modes
    ## Mode 1
    In this mode you stage a change to the config but don't apply it until the function gets called in the second mode

    Raises ValueError if the option does not exist in the config in the given section 

    ### Arguments
    section: the section of the config you want to change
    option: the option of the config you want to change
    value: the value you want to be the option
    apply: you can completely ignore this it does not serve a function in the first mode

    ## Mode 2
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
    elif apply == True and section is not None:
        if config.has_option(section, option):
            config.set(section, option, value)
            with open('config.ini', 'w') as f:
                config.write(f)
            logger.info('Applied value change to config directly')
        else:
            # If the option doesn't exist in the section
            raise ValueError(f'The option "{option}" in the section "{section}" does not exist')

def applyConfigUpdates():
    """Applies the staged config to the current config and writes it to the config file"""
    global stagedConfig
    
    if len(stagedConfig) > 0:
        for section in stagedConfig.keys():
            for option in stagedConfig[section]:
                value = stagedConfig[section][option]
                config.set(section, option, value)
        with open('config.ini', 'w') as f:
            config.write(f)
        stagedConfig.clear()

        # tries to make the Apply Button in the SettingsWindow unpressable again
        try:
            ApplyBtn['state'] = 'disabled'
        except NameError:
            pass
        logger.info('Applied all staged changes to the config')
    else:
        logger.info('There are no staged changes that could be applied')


def CheckForUpdates(automatic: bool = True, pVersion: str = None):
    """Checks for updates of the software and gives the user an installation prompt if an update was found
    If the automatic parameter is False it additionally gives the user a prompt for when there was no update or no connection to the server
    If pVersion is provided, it is given as a means to check for updates instead of the version variable"""
    if isinstance(pVersion, str):
        new_update = updater.CheckNewVersion(pVersion, 'https://github.com/jasger9000/Cryptographer/')
    else:
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

def InstallNewLanguage():
    # Window Config
    InstallWindow = Toplevel(root)
    InstallWindow.title(getTranslation('SettingsMenu', 'addNewLanguage'))
    InstallWindow.resizable(0,0)
    InstallWindow.focus()
    InstallWindow.transient(root)
    InstallWindow.grab_set()
    logger.info('Loaded Window config')

    Label(InstallWindow, text=getTranslation('SettingsMenu', 'addNewLanguage') , font=('Helvetica', 14, font.BOLD, UNDERLINE)).grid(row=0, column=0, columnspan=2, pady=3)
    
    frame = Frame(InstallWindow)
    frame.grid(row=1, column=0, padx=10, pady=12)

    # Gets List of installed Languages
    langList = []
    for entry in os.scandir(f'{os.getcwd()}/Languages'):
        if entry.is_file() and entry.name.rsplit('.')[1] == 'json':
            langList.append(entry.name.rsplit('.')[0])
    
    # Requests the Languages from Github
    gitLangs = []
    for item in updater.getItems('https://github.com/jasger9000/Cryptographer', 'Languages'):
        if item.rsplit('.')[1] == 'json':
            gitLangs.append(item.rsplit('.')[0])
        print(item, item[-3:])
    
    # Creates List of installable Languages
    newLangs = []
    for item in gitLangs:
        if item not in langList:
            newLangs.append(item)

    langBox = Combobox(frame, values=newLangs, state='readonly')
    InstallBtn = Button(frame, text=getTranslation('SettingsMenu', 'installBtn'), command=lambda: [updater.DownloadFile('https://github.com/jasger9000/Cryptographer', langBox.get() + '.json', 'master/Languages', 'Languages')])
    InstallBtn.grid(row=1, column=1)
    if len(newLangs) == 0:
        langBox.set(getTranslation('SettingsMenu', 'noLanguagesAvailable'))
        InstallBtn['state'] = 'disabled'

    langBox.grid(row=1, column=0)

def LoadLang(l):
    """Loads a Language pack if it is installed and asks the user to reinstall the English one if the users and the English one is missing.
    Returns the language pack if it is installed otherwise returns None"""
    if os.path.exists('Languages'):
        logger.info('Loading Language')

        if os.path.exists(f'Languages/{l}.json'): # Checks if Language pack exists and loads it if it does
            with open(f'Languages/{l}.json', 'r', encoding='UTF-8') as f:
                lang = json.load(f)
            logger.info('Loaded ' + l + ' Language pack')
        elif os.path.exists('Languages/English.json'): # Checks if English Language pack is installed to try to fallback
            logger.error('Language not found, continuing with English')
            messagebox.showerror("Language not found", "Couldn't find the Language you are trying to use, please reinstall the Language pack")
            with open('Languages/English.json', 'r', encoding='UTF-8') as f:
                lang = json.load(f)
            UpdateConfig('Settings', 'Language', "English")
        else: # Asks the user to reinstall the English Language pack
            logger.exception('English Language pack not installed')
            messagebox.showerror('English not found', 'Cryptographer tried to fallback to English but failed because English is not installed.\nPlease reinstall the English Language pack.')
            if messagebox.askyesno('Reinstall English', 'Reinstall English Language pack?'):
                logger.info('Trying to reinstall English')
                if updater.DownloadFile('https://github.com/jasger9000/Cryptographer', 'English.json', 'master/Languages', 'Languages'):
                    UpdateConfig('Settings', 'Language', "English")
                    with open('Languages/English.json', 'r', encoding='UTF-8') as f:
                        lang = json.load(f)
                else:
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

def getTranslation(groupKey: str, itemKey: str, *replacements):
    """Gets a translation for a given key from the language pack
    If replacements is given, the arguments will replace %s in the translation value"""
    global lang

    try:
        # checks if replacements is used
        if len(replacements) == 0:
            return lang[groupKey][itemKey]
        else:
            return lang[groupKey][itemKey] % replacements
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


def Copy():
    """Copies the output from the entry to the users clipboard"""
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
    """Deletes the output from the entry"""
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


def OpenSettings():
    """Opens the Settings Window"""
    global langBox, ApplyBtn, stagedConfig

    # Setting Window config
    logger.info('Opening Settings window')

    SettingsWindow = Toplevel(root)
    SettingsWindow.title(getTranslation('window', 'settingsWindowTitle'))
    SettingsWindow.iconbitmap(resourcePath('UI/settings.ico'))
    SettingsWindow.resizable(0,0)
    SettingsWindow.focus()
    SettingsWindow.transient(root)
    SettingsWindow.grab_set()
    SettingsWindow.protocol("WM_DELETE_WINDOW", lambda: [stagedConfig.clear(), logger.info('cleared all staged Config changes because Settings Window was closed'), SettingsWindow.destroy()])
    logger.info('Loaded Window config')
    
    Label(SettingsWindow, text=getTranslation('window', 'settingsWindowTitle') , font=('Helvetica', 14, font.BOLD, UNDERLINE)).grid(row=0, column=0, pady=12)
    SettingsFrame = Frame(SettingsWindow)
    SettingsFrame.grid(row=1, column=0, padx=20)

    frame = Frame(SettingsWindow)
    frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 12))

    Label(SettingsFrame, text=getTranslation('SettingsMenu', 'general'), font=('Helvetica', 8, font.BOLD, UNDERLINE)).grid(row=0, column=0, pady=(12, 2))

    # Language Setting
    Label(SettingsFrame, text=getTranslation('SettingsMenu', 'languageOptionLabel')).grid(row=1, column=0, pady=5)
    langList = [entry.name.strip('.json') for entry in os.scandir('Languages') if entry.is_file() and os.path.splitext(entry.name)[1] == '.json']
    langBox = Combobox(SettingsFrame, values=langList, state='readonly')
    langBox.set(config['Settings']['language'])
    langBox.bind('<<ComboboxSelected>>', lambda event: UpdateConfig('Settings', 'language', langBox.get()))
    langBox.grid(row=1, column=1, pady=5)
    Button(SettingsFrame, text=getTranslation('SettingsMenu', 'addNewLanguage'), command=InstallNewLanguage).grid(row=1, column=2, pady=5)

    # Save key?
    SaveLabel = Label(SettingsFrame, text=getTranslation('SettingsMenu', 'rememberKeyOptionLabel'))
    SaveLabel.grid(row=2, column=0, pady=5)
    ToolTip(SaveLabel, msg=getTranslation('SettingsMenu', 'rememberKeyOptionTip'))
    saveKey = IntVar(value=config.getint('Settings', 'savelastkey'))
    Checkbutton(SettingsFrame, variable=saveKey, onvalue=1, offvalue=0, command=lambda: [
        UpdateConfig('Settings', 'SaveLastKey', str(saveKey.get())), 
        UpdateConfig('State', 'keyfile', 'None'), 
        UpdateConfig('State', 'publickeyfile', 'None'), 
        UpdateConfig('State', 'privatekeyfile', 'None')
        ]).grid(row=2, column=1, pady=5)

    # Automatic CFU?
    Label(SettingsFrame, text=getTranslation('SettingsMenu', 'autoCFUOptionLabel')).grid(row=3, column=0, pady=5, padx=(0, 20))
    autoCFU = IntVar(value=config['Settings']['CFUatStartup'])
    Checkbutton(SettingsFrame, variable=autoCFU, onvalue=1, offvalue=0, command=lambda: UpdateConfig('Settings', 'CFUatStartup', str(autoCFU.get()))).grid(row=3, column=1, pady=5)

    # Light/Dark/Windows mode
    Label(SettingsFrame, text=getTranslation('SettingsMenu', 'themes'), font=('Helvetica', 8, font.BOLD, UNDERLINE)).grid(row=4, column=0, pady=(12, 2))

    theme = IntVar(value=config['Settings']['theme'])
    Label(SettingsFrame, text=getTranslation('SettingsMenu', 'lightTheme')).grid(row=5, pady=5)
    Radiobutton(SettingsFrame, variable=theme, value=1, command=lambda: UpdateConfig('Settings', 'theme', str(theme.get()))).grid(row=5, column=1, pady=5)

    Label(SettingsFrame, text=getTranslation('SettingsMenu', 'darkTheme')).grid(row=6, pady=5)
    Radiobutton(SettingsFrame, variable=theme, value=2, command=lambda: UpdateConfig('Settings', 'theme', str(theme.get()))).grid(row=6, column=1, pady=5)
    
    # Default and Apply Button
    DefaultBtn = Button(frame, text=getTranslation('SettingsMenu', 'defaultBtn'), command=lambda: [generateConfig(), root.destroy(), os.startfile(f'{os.getcwd()}/Cryptographer.exe')])
    DefaultBtn.grid(row=0, pady=5)
    ApplyBtn = Button(frame, state='disabled',text=getTranslation('SettingsMenu', 'applyBtn'), command=applyConfigUpdates)
    ApplyBtn.grid(row=0, column=1, pady=5)
    
    logger.info('Finished loading')
    root.wait_window()


def SwitchMode(switchMode: str):
    """Switches from Symmetric to Asymmetric Cryptography mode and back"""
    global currentMode, imgLoadedTrue, imgLoadedFalse
    
    logger.info('Switching mode')

    imgLoadedTrue = ImageTk.PhotoImage(Image.open(resourcePath('UI/Loaded.ico')).resize((40, 40)))
    imgLoadedFalse = ImageTk.PhotoImage(Image.open(resourcePath('UI/NotLoaded.ico')).resize((40, 40)))
    if currentMode == switchMode:
        logger.info('Aborted switching because Software is already in the right mode')
    elif switchMode == 'Symmetric':
        windowFrames()

        # Key Loaded Indicator
        if  config['Settings']['savelastkey'] == 1 and config['State']['keyfile'] != 'None':
            key = config['State']['keyfile']
            Indicator = Label(KeyFrame, image=imgLoadedTrue) # LoadIndicator 
            IndicatorTooltip = ToolTip(Indicator, msg=getTranslation('window', 'indicatorTooltip', getTranslation('Phrases', 'loaded')), delay=1.0) # Tooltip for LoadIndicator
        else:
            key = ''
            Indicator = Label(KeyFrame, image=imgLoadedFalse) # LoadIndicator
            IndicatorTooltip = ToolTip(Indicator, msg=getTranslation('window', 'indicatorTooltip', getTranslation('Phrases', 'notLoaded')), delay=1.0) # Tooltip for LoadIndicator
        Indicator.grid(row=0, column=0, pady=10)
        Button(KeyFrame, text=getTranslation('Phrases', 'browse'), command=thisNeedsToBeReplaced).grid(row=1, column=0, pady=2) #TODO MAKE COMMAND Browse Dialog METHOD
        Button(KeyFrame, text=getTranslation('window', 'generateKeyBtn'), command=thisNeedsToBeReplaced).grid(row=2, column=0, padx=10, pady=6) #TODO MAKE COMMAND GENERATE KEY METHOD

        root.title(f'{getTranslation("window", "symTitle")} {version}')
        TitleLabel.config(text=getTranslation('window', 'symTitle'))
        UpdateConfig('State', 'mode', 'Symmetric', True)
    elif switchMode == 'Asymmetric':
        #TODO here needs to be the asymWindow function
        root.title(f'{getTranslation("window", "asymTitle")} {version}')
        TitleLabel.config(text=getTranslation('window', 'asymTitle'))
        UpdateConfig('State', 'mode', 'Asymmetric', True)
    else:
        raise ValueError(f'The mode given is not valid (mode given {switchMode}) please use "Symmetric" or "Asymmetric"')
    currentMode = switchMode
    logger.info('switching complete')

def windowFrames():
    """Loads the frames used for the Cryptography function just destroys the children of them if they already do"""
    global MessageFrame, FileFrame, KeyFrame

    # tries to destroy every child of the frames and if they don't exist already load them first
    try:
        for child in KeyFrame.winfo_children():
            child.destroy()
        logger.info()
    except NameError:
        # Tab Register
        TabRegister = Notebook(root)
        TabRegister.grid(row=1, column=0, padx=20)

        # Tabs
        MessageFrame = Frame(TabRegister)
        FileFrame = Frame(TabRegister)

        MessageFrame.pack(fill='both', expand=1)
        FileFrame.pack(fill='both', expand=1)

        TabRegister.add(MessageFrame, text=getTranslation('Phrases', 'message'))
        TabRegister.add(FileFrame, text=getTranslation('Phrases', 'file'))

        # Key frame
        KeyFrame = LabelFrame(root, text=getTranslation('Phrases', 'key'))
        KeyFrame.grid(row=1, column=1, padx=10)
    
    # Message Tab
    Label(MessageFrame, text='\n' + getTranslation('window', 'encryptMessageTitle')).grid(row=0, column=0)
    EncryptMessageEntry = Entry(MessageFrame, width=40) # Define Entry
    EncryptMessageEntry.grid(row=1, column=0, padx=5) # Put Entry on screen
    Button(MessageFrame, text=getTranslation('Phrases', 'encrypt'), command=thisNeedsToBeReplaced).grid(row=1, column=1) # Encrypt Btn #TODO MAKE THE COMMAND THE ENCRYPT METHOD

    Label(MessageFrame, text='\n\n' + getTranslation('window', 'decryptMessageTitle')).grid(row=2, column=0) # Description Label
    DecryptMessageEntry = Entry(MessageFrame, width=40) # Define Entry
    DecryptMessageEntry.grid(row=3, column=0, padx=5, pady=5) # Put Entry on screen
    Button(MessageFrame, text=getTranslation('Phrases', 'decrypt'), command=thisNeedsToBeReplaced).grid(row=3, column=1) # Decrypt Btn #TODO MAKE THE COMMAND THE DECRYPT METHOD

    # File Tab
    Label(FileFrame, text='\n' + getTranslation('window', 'encryptFileTitle')).grid(row=0, column=0) # Description Label
    EncryptFileEntry = Entry(FileFrame, width=40) # Define Entry
    EncryptFileEntry.grid(row=1, column=0, padx=5) # Put Entry on screen
    Button(FileFrame, text=getTranslation('Phrases', 'encrypt'), command=thisNeedsToBeReplaced).grid(row=1,column=1) # Encrypt Btn #TODO MAKE THE COMMAND THE ENCRYPT METHOD
    Button(FileFrame, text=getTranslation('Phrases', 'browse'), command=thisNeedsToBeReplaced).grid(row=1, column=2, padx=(0,5)) # BrowseCryptographyDialog #TODO MAKE THE COMMAND THE Browse Dialog METHOD

    Label(FileFrame, text='\n\n' + getTranslation('window', 'decryptFileTitle')).grid(row=2, column=0) # Description Label
    DecryptFileEntry = Entry(FileFrame, width=40) # Define Entry
    DecryptFileEntry.grid(row=3, column=0, padx=5, pady=5) # Put Entry on screen
    Button(FileFrame, text=getTranslation('Phrases', 'decrypt'), command=thisNeedsToBeReplaced).grid(row=3,column=1) # Decrypt Btn #TODO MAKE THE COMMAND THE DECRYPT METHOD
    Button(FileFrame, text=getTranslation('Phrases', 'browse'), command=thisNeedsToBeReplaced).grid(row=3, column=2, padx=(0,5)) # BrowseDecryptDialog #TODO MAKE THE COMMAND THE Browse Dialog METHOD

def thisNeedsToBeReplaced():
    pass

def main():
    global root, out, lang, TitleLabel, currentMode, config

    # Tk Config
    root = Tk()

    root.resizable(0,0)
    TitleLabel = Label(root, text='', font=('Helvetica', 14, font.BOLD, UNDERLINE)) # text will change when loading a mode
    TitleLabel.grid(row=0, column=0, columnspan=2, pady=12)
    updater.addFileHandlerLogging(logFile)
    config, lang = LoadConfig()
    if not lang:
        return

    # Tries to make the title, if the version variable does not exist and insert the icon
    try:
        root.title(f'Cryptographer {version}')
        root.iconbitmap('Cryptographer.exe')
    except TclError:
        # Gets triggered if the icon does not exist, this is only possible while programming so it can just be passed
        logger.warning("Couldn't find icon, continuing without")
    except NameError:
        # Gets triggered if the version variable is not found which is most likely because of my stupidity of accidentally deleting the version variable
        # ask the user to reinstall the software
        logger.error("Could not find Version variable, corruption likely")
        root.title(getTranslation('versionNotFound', 'Title'))
        root.bell()
        
        if messagebox.askokcancel(getTranslation('versionNotFound', 'Title'), getTranslation('versionNotFound', 'Message')):
            CheckForUpdates(False, 'v0.0.0')
        else:
            return

    # initialises variable that keeps track of the current mode the application is in can be 'Symmetric' or 'Asymmetric'
    currentMode = ''

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
    # HelpMenu.add_command(label=getTranslation('menuBar', 'about'))
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