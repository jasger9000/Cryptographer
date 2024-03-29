import importlib
from urllib.error import URLError
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
import sys

sys.path.insert(0, f'{os.getcwd()}/Languages') 

# logger config
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')

# fileHandler config
fileHandler = logging.FileHandler('Cryptographer.log')
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(fmt)
logger.addHandler(fileHandler)
with open('Cryptographer.log', 'w') as f:
    f.write('')

# streamHandler config
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(fmt)
streamHandler.setLevel(logging.DEBUG)
logger.addHandler(streamHandler)

version = 'v0.7.1'
stagedConfig = {}

def LoadFileTypes(lang):
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

def LoadLang(l: str):
    if os.path.exists('Languages'):
        if type(l) is not str:
            l = langBox.get()
        try:
            lang = importlib.import_module(l)
            if lang.version < 1:
                logger.critical('Language pack too old')
                messagebox.showerror('Language pack too old', 'The Language pack you are using is too old, please install a newer version')
                return None
            UpdateConfig('Settings', 'Language', l)
        except ModuleNotFoundError:
            logger.error('Language Module not found, continuing with English')
            try:
                messagebox.showerror("Language not found", "Couldn't find the Language you are trying to use, please reinstall the Language pack")
                UpdateConfig('Settings', 'Language', l)
                lang = importlib.import_module('English')
                if lang.version < 1:
                    return None
            except ModuleNotFoundError:
                logger.exception('English Language pack not installed')
                messagebox.showerror('English not found', 'Cryptographer tried to fallback to English but failed because English is not installed.\nPlease reinstall the English Language pack.')
                if messagebox.askyesno('Reinstall English', 'Reinstall English Language pack?'):
                    try:
                        logger.info('Trying to reinstall English')
                        request.urlretrieve(f'https://raw.githubusercontent.com/jasger9000/Cryptographer/master/Languages/English.py', f'Languages/English.py')
                    except URLError:
                        logger.error('Connection could not be established')
                        messagebox.showerror("Couldn't reinstall English", "Couldn't reinstall English because connection to Github couldn't be Established.\nPlease try again later or check if you are Connected to the Internet.")
                        return None
                else:
                    return None
        return lang
    else:
        logger.error('Language folder not found, creating new')
        os.mkdir('/Languages')
        LoadLang('')


def LoadConfig(Force: bool = False):
    global config
    config = ConfigParser()

    logger.info('Searching for config')
    if os.path.exists('config.ini') is False or Force is True:
        logger.warning('Config not found, generating new')
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
        lang = LoadLang('English')
        logger.info('New Config generated')
    else:
        logger.info('Config found, loading...')
        config.read('config.ini')

        if int(config['State']['Version']) < 1:
            logger.warning('Config too old generating new')
            os.remove('config.ini')
            LoadConfig(True)
        else:
            lang = LoadLang(config['Settings']['Language'])
            logger.info('Using Language: ' + config['Settings']['Language'])
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


def OpenSettings():
    global langBox, ApplyBtn, Settings, langList
    logger.info('Opening Settings')

    # Window Config
    Settings = Toplevel(root)
    Settings.title(lang.CryptMain['HelpSettingsLabel'])
    Settings.iconbitmap(resource_path('UI/Settings.ico'))
    Settings.resizable(0,0)
    Settings.focus()
    Settings.transient(root)
    Settings.grab_set()
    logger.info('Loaded Window config')

    
    Label(Settings, text=lang.CryptMain['HelpSettingsLabel'] , font=('Helvetica', 14, font.BOLD, UNDERLINE)).grid(row=0, column=0, pady=12)
    SettingsFrame = Frame(Settings)
    SettingsFrame.grid(row=1, column=0, padx=20)

    frame = Frame(Settings)
    frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 12))

    Label(SettingsFrame, text=lang.SettingsLabels['General'], font=('Helvetica', 8, font.BOLD, UNDERLINE)).grid(row=0, column=0, pady=(12, 2))

    # Language Setting
    Label(SettingsFrame, text=lang.SettingsLabels['LangLabel']).grid(row=1, column=0, pady=5)
    langList = [entry.name.strip('.py') for entry in os.scandir('Languages') if entry.is_file() and os.path.splitext(entry.name)[1] == '.py']
    langBox = Combobox(SettingsFrame, values=langList, state='readonly')
    langBox.set(lang.Language)
    langBox.bind('<<ComboboxSelected>>', LoadLang)
    langBox.grid(row=1, column=1, pady=5)
    Button(SettingsFrame, text=lang.SettingsLabels['AddLangBtn'], command=InstallNewLanguage).grid(row=1, column=2, pady=5)

    # Save key?
    SaveLabel = Label(SettingsFrame, text=lang.SettingsLabels['RememberKeyLabel'])
    SaveLabel.grid(row=2, column=0, pady=5)
    ToolTip(SaveLabel, msg=lang.SettingsLabels['RememberKeyTip'])
    saveKey = IntVar(value=config.getint('Settings', 'savelastkey'))
    Checkbutton(SettingsFrame, variable=saveKey, onvalue=1, offvalue=0, command=lambda: [UpdateConfig('Settings', 'SaveLastKey', str(saveKey.get())), UpdateConfig('State', ['keyfile', 'publickeyfile', 'privatekeyfile'], 'None')]).grid(row=2, column=1, pady=5)

    # Automatic CFU?
    Label(SettingsFrame, text=lang.SettingsLabels['AutoCFULabel']).grid(row=3, column=0, pady=5, padx=(0, 20))
    autoCFU = IntVar(value=config['Settings']['CFUatStartup'])
    Checkbutton(SettingsFrame, variable=autoCFU, onvalue=1, offvalue=0, command=lambda: UpdateConfig('Settings', 'CFUatStartup', str(autoCFU.get()))).grid(row=3, column=1, pady=5)

    # Light/Dark/Windows mode
    Label(SettingsFrame, text=lang.SettingsLabels['Themes'], font=('Helvetica', 8, font.BOLD, UNDERLINE)).grid(row=4, column=0, pady=(12, 2))

    theme = IntVar(value=config['Settings']['theme'])
    Label(SettingsFrame, text=lang.SettingsLabels['LightTheme']).grid(row=5, pady=5)
    Radiobutton(SettingsFrame, variable=theme, value=1, command=lambda: UpdateConfig('Settings', 'theme', str(theme.get()))).grid(row=5, column=1, pady=5)

    Label(SettingsFrame, text=lang.SettingsLabels['DarkTheme']).grid(row=6, pady=5)
    Radiobutton(SettingsFrame, variable=theme, value=2, command=lambda: UpdateConfig('Settings', 'theme', str(theme.get()))).grid(row=6, column=1, pady=5)

    # Label(SettingsFrame, text='Sync theme').grid(row=7, pady=5) # ! NEEDS TO CHANGE WITH LANG
    # Radiobutton(SettingsFrame, variable=theme, value=3, command=lambda: UpdateConfig('Settings', 'theme', str(theme.get()))).grid(row=7, pady=5)

    
    # Default and Apply Button
    DefaultBtn = Button(frame, text=lang.SettingsLabels['DefaultBtn'], command=lambda: [LoadConfig(True), root.destroy(), os.startfile(f'{os.getcwd()}/Cryptographer.exe')])
    DefaultBtn.grid(row=0, pady=5)
    ApplyBtn = Button(frame, state='disabled',text=lang.SettingsLabels['ApplyBtn'], command=ApplyChanges)
    ApplyBtn.grid(row=0, column=1, pady=5)
    
    logger.info('Finished loading')
    root.wait_window()

def ApplyChanges():
    root.destroy()

    for option in stagedConfig:
        section, value = stagedConfig.get(option)
        config.set(section, option, value)
    with open('config.ini', 'w') as f:
        config.write(f)
    os.startfile(f'{os.getcwd()}/Cryptographer.exe')


def InstallNewLanguage():
    global langBox

    # Window Config
    InstallWindow = Toplevel(Settings)
    InstallWindow.title(lang.CryptMain['SettingsLangLabel'])
    InstallWindow.iconbitmap(resource_path('UI/download.ico'))
    InstallWindow.resizable(0,0)
    InstallWindow.focus()
    InstallWindow.transient(Settings)
    InstallWindow.grab_set()
    logger.info('Loaded Window config')

    Label(InstallWindow, text=lang.CryptMain['SettingsLangLabel'] , font=('Helvetica', 14, font.BOLD, UNDERLINE)).grid(row=0, column=0, columnspan=2, pady=3)
    
    frame = Frame(InstallWindow)
    frame.grid(row=1, column=0, padx=10, pady=12)


    # Requests the Languages from Github
    try:
        for i in requests.get('https://api.github.com/repos/jasger9000/Cryptographer/git/trees/master').json()['tree']:
            if i['path'] == 'Languages':
                gitLangs = [item['path'].rstrip('.py') for item in requests.get(f'https://api.github.com/repos/jasger9000/Cryptographer/git/trees/{i["sha"]}').json()['tree'] if os.path.splitext(item['path'])[1] == '.py']
    except requests.ConnectionError:
        logger.warning("Couldn't connect to server")
        gitLangs = ''
        
    newLangs = [i for i in gitLangs if i not in langList] # Creates List of installable Languages

    newLangBox = Combobox(frame, values=newLangs, state='readonly')
    InstallBtn = Button(frame, text=lang.SettingsLabels['AddLangBtn'], command=lambda: [
        request.urlretrieve(f'https://raw.githubusercontent.com/jasger9000/Cryptographer/master/Languages/{newLangBox.get()}.py', f'Languages/{newLangBox.get()}.py'), 
        newLangs.remove(newLangBox.get()),
        langList.append(newLangBox.get()),
        newLangBox.config(values=newLangs),
        newLangBox.update(),
        newLangBox.set(''),
        langBox.config(values=langList),
        langBox.update()
        ])

    InstallBtn.grid(row=1, column=1)
    if len(gitLangs) == 0:
        newLangBox.set(lang.Messages['ConnectErrLang'])
        InstallBtn['state'] = 'disabled'
    elif len(newLangs) == 0:
        newLangBox.set(lang.Messages['NoNewLang'])
        InstallBtn['state'] = 'disabled'

    newLangBox.grid(row=1, column=0)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def SwitchMode(mode: str):
    if TitleLabel.cget('text') == '' or config['State']['Mode'] != mode:
        logger.info('Switching Mode')
        try:
            if EncryptFrame.winfo_exists():
                EncryptFrame.destroy()
                DecryptFrame.destroy()
                KeyFrame.destroy()
        except NameError:
            pass
        LoadFrames()
        root.geometry('')

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
    except requests.ConnectionError:
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
        threading.Thread(target=lambda: CheckForUpdates('automatic')).start()

    if config['State']['Mode'] == 'Symmetric':
        SwitchMode('Symmetric')
    elif config['State']['Mode'] == 'Asymmetric':
        SwitchMode('Asymmetric')
    root.mainloop()


if __name__ == '__main__':
    main()