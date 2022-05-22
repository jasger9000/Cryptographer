import Asym_Cryptographer
import Sym_Cryptographer
from tkinter import messagebox, Tk, Menu, TclError
import logging
import requests
from packaging.version import parse
import webbrowser
from urllib import request
from os import getcwd, remove, path, startfile
import zipfile


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

version = 'ver. 0.5.0'

def switchSymmetric(root: Tk):
    global frameA0, frameA1, frameA2, frameA3, TitleLabelA, frameB0, frameB1, frameB2, frameB3, TitleLabelB

    if 'frameA0' not in globals() or frameA0 is None:       
        logger.info('switching to Symmetric Cryptographer')
        try:
            Asym_Cryptographer.Unload(frameB0, frameB1, frameB2, frameB3, TitleLabelB)
            frameB0 = frameB1 = frameB2 = frameB3 = TitleLabelB = None
        except NameError:
            pass
        frameA0, frameA1, frameA2, frameA3, TitleLabelA = Sym_Cryptographer.main(root, version)
    logger.info('switching complete')

def switchAsymmetric(root: Tk):
    global frameA0, frameA1, frameA2, frameA3, TitleLabelA, frameB0, frameB1, frameB2, frameB3, TitleLabelB

    if 'frameB0' not in globals() or frameB0 is None:   
        logger.info('switching to Asymmetric Cryptographer')
        try:
            Sym_Cryptographer.Unload(frameA0, frameA1, frameA2, frameA3, TitleLabelA)
            frameA0 = frameA1 = frameA2 = frameA3 = TitleLabelA = None
        except NameError:
            pass
        frameB0, frameB1, frameB2, frameB3, TitleLabelB = Asym_Cryptographer.main(root, version)
    logger.info('switching complete')


def CheckForUpdates():
    try:
        logger.info('Trying to get latest version')
        latest = requests.get('https://api.github.com/repos/Panakotta00/FicsIt-Networks/releases/latest').json()['tag_name']
        logger.info('Got latest version')
        if parse(latest) > parse(version):
            logger.info('Newer Version found')
            return True
        else:
            logger.info('No new version found')        
    except Exception:
        pass

def InstallNewUpdate(root: Tk):
    logger.info('Downloading Update')
    # r = requests.get(f'https://github.com/jasger9000/Cryptographer/releases/download/{latest}/Cryptographer.zip')
    file = f'{getcwd()}/Cryptographer.zip'
    url = f'https://github.com/Panakotta00/FicsIt-Networks/releases/download/0.3.4/Ficsit-Networks-0.3.4.zip'
    request.urlretrieve(url, file)
    logger.info('Update downloaded')

    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(getcwd())
    logger.info('Extracted Update')

    if path.exists(file):
        remove(file)
    logger.info('Finished installing, restarting now')
    startfile('Cryptographer.exe')
    root.destroy()

def CheckForUpdates2(root: Tk):
    logger.info('Manual Update Checking initialised')
    newUpdate = CheckForUpdates()
    if newUpdate:
        userConfirm = messagebox.askyesno('New version available', "There's a new version available for download.\n Would you like to download it?")
        if userConfirm:
            InstallNewUpdate(root)
    else:
        messagebox.showinfo('No Update found', 'There was no new Update found, that could be installed')


def main():
    # root Config
    root = Tk()
    root.resizable(0,0)
    root.geometry('300x300')
    try:
        root.title(f'Cryptographer {version}')
        root.iconbitmap('Cryptographer.exe')
    except TclError:
        logger.warn("Couldn't find icon, continuing without")
    except NameError:
        logger.error("Could not find Version variable, corruption likely")
        root.title('Version not found!')
        userConfirm = messagebox.askokcancel("Version not found", "The Software you are currently using doesn't have a Version registered to it, please reinstall the Software.\nIf you have already done this please open a issue in my github.")
        if userConfirm:
                # r = requests.get(f'https://github.com/jasger9000/Cryptographer/releases/download/{latest}/Cryptographer.exe')
                r = f'https://github.com/Panakotta00/FicsIt-Networks/releases/download/0.3.4/Ficsit-Networks-0.3.4.zip'
        else:
            root.destroy()

    menubar = Menu(root)
    ModeMenu = Menu(menubar, tearoff=0)
    ModeMenu.add_command(label='Symmetric', command=lambda: switchSymmetric(root))
    ModeMenu.add_command(label='Asymmetric', command=lambda: switchAsymmetric(root))
    menubar.add_cascade(label='Mode', menu=ModeMenu)

    HelpMenu = Menu(menubar, tearoff=0)
    HelpMenu.add_command(label='Open Github Page', command=lambda: webbrowser.open('https://github.com/jasger9000/Cryptographer'))
    HelpMenu.add_command(label='Check For Updates', command=lambda: CheckForUpdates2())
    menubar.add_cascade(label='Help', menu=HelpMenu)
    root.config(menu=menubar)

    newUpdate = CheckForUpdates()
    if newUpdate:
        userConfirm = messagebox.askyesno('New version available', "There's a new version available for download.\n Would you like to download it?")
        if userConfirm:
            InstallNewUpdate(root)

    root.mainloop()


if __name__ == '__main__':
    main()

# TODO Save which state was last used
# TODO Check for Updates Btn