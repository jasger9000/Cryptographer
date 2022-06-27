<<<<<<< HEAD
from tkinter import UNDERLINE, filedialog, messagebox, Tk, Label, Button, Entry, LabelFrame
from tkinter.font import BOLD
=======
from tkinter import UNDERLINE, filedialog, messagebox
from tktooltip import ToolTip 
from PIL import ImageTk, Image
from tkinter.ttk import Button, Frame, Label, Entry, LabelFrame
>>>>>>> dev
from cryptography.fernet import Fernet
import rsa
import base64
import logging
<<<<<<< HEAD
from pathlib import Path
from os.path import expandvars, getsize
from os import getcwd

=======
import pathlib
import os
>>>>>>> dev

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


<<<<<<< HEAD
fileTypes = (
    ('Text Files', ('*.txt', '*.doc', '*.docx', '*.log', '*.msg', '*.odt', '*.pages', '*.rtf', '*.tex', '*.wpd', '*.wps')),
    ('Video Files', ('*.mp4', '*.mov', '*.avi', '*.flv', '*.mkv', '*.wmv', '*.avchd', '*.webm', '*MPEG-4', '*.H.264')),
    ('Audio Files', ('*.aif', '*.aiff', '*.iff', '*.m3u', '*.m4a', '*.mp3', '*.mpa', '*.wav', '*.wma', '*.aup3', '*.aup', '*.ogg', '*.mp2')),
    ('Picture Files', ('*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp', '*.raw', '*.tiff', '*.psd', '*.cr2')),
    ('All Files', '*.*'),
    ('Encrypted Files', '*.Encrypted'),
    ('Private Key files', '*.priv_key'),
    ('Public Key files', '*.pub_key'),
)


=======
>>>>>>> dev
class fileNotFoundError(FileNotFoundError):
    pass
class PrivKeyNotFoundError(FileNotFoundError):
    pass
class PubKeyNotFoundError(FileNotFoundError):
    pass

<<<<<<< HEAD
def BrowseKeyDialog(keyEntry: Entry, mode: str):
    if mode == 'Private':
        type = 'priv_key'
    else:
        type = 'pub_key'
    browseKeyDialog = filedialog.askopenfilename(initialdir=expandvars(R'C:\Users\$USERNAME\Documents'), title=f'Open {mode} Key...', filetypes=((f'{mode} Key files', f'*.{type}'), fileTypes[4]))
    if browseKeyDialog:
        logger.info(f'User selected {mode} ')
        keyEntry.delete(0,"end")
        keyEntry.insert(0, browseKeyDialog)

def BrowseEncryptDialog(encrypt2Entry: Entry):
    browseEncryptDialog = filedialog.askopenfilename(initialdir=expandvars(R'C:\Users\$USERNAME\Documents'), title=f'Select file to Encrypt...', filetypes=(fileTypes[0], fileTypes[1], fileTypes[2], fileTypes[3], fileTypes[4]))
=======
def BrowseKeyDialog(mode: str, KeyFrame: Frame):
    global img1, IndicatorTooltip1, Indicator1, Indicator2, IndicatorTooltip2, img2, pubKey, privKey

    if mode == 'Private':
        type = 7
    else:
        type = 8
    
    key = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=lang.Dialog['Open'] + lang.Dialog[mode], filetypes=(fileTypes[type], fileTypes[4]))
    
    if mode == 'Public':
        pubKey = key
        if key != '':
            img1 = ImageTk.PhotoImage(Image.open('UI/Loaded.ico').resize((40, 40)))
            Indicator1 = Label(KeyFrame, image=img1) # LoadIndicator
            Indicator1.grid(row=1, column=1, padx=5)
            IndicatorTooltip1 = ToolTip(Indicator1, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['Loaded'], delay=1.0) # Tooltip for LoadIndicator
    else:
        privKey = key
        if key != '':
            img2 = ImageTk.PhotoImage(Image.open('UI/Loaded.ico').resize((40, 40)))
            Indicator2 = Label(KeyFrame, image=img2) # LoadIndicator
            Indicator2.grid(row=4, column=1, padx=5)
            IndicatorTooltip2 = ToolTip(Indicator2, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['Loaded'], delay=1.0) # Tooltip for LoadIndicator


def BrowseEncryptDialog(encrypt2Entry: Entry):
    browseEncryptDialog = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=lang.Dialog['Open'] + lang.Dialog['file'] + lang.Dialog['to'] + lang.Dialog['Encrypt'], filetypes=(fileTypes[0], fileTypes[1], fileTypes[2], fileTypes[3], fileTypes[4]))
>>>>>>> dev
    if browseEncryptDialog:
        logger.info('User selected file to Encrypt')
        encrypt2Entry.delete(0,"end")
        encrypt2Entry.insert(0, browseEncryptDialog)

def BrowseDecryptDialog(decrypt2Entry: Entry):
<<<<<<< HEAD
    browseDecryptDialog = filedialog.askopenfilename(initialdir=expandvars(R'C:\Users\$USERNAME\Documents'), title=f'Select file to Decrypt...', filetypes=(fileTypes[5], fileTypes[0]))
=======
    browseDecryptDialog = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=lang.Dialog['Open'] + lang.Dialog['file'] + lang.Dialog['to'] + lang.Dialog['Decrypt'], filetypes=(fileTypes[5], fileTypes[0]))
>>>>>>> dev
    if browseDecryptDialog:
        logger.info('User selected file to Decrypt')
        decrypt2Entry.delete(0,"end")
        decrypt2Entry.insert(0, browseDecryptDialog) 

<<<<<<< HEAD
def GenerateKeyPair(keyEntry: Entry):
    logger.info('Initiated GenerateKeyPair')
    publickeyPath = filedialog.asksaveasfilename(initialdir=expandvars(R'C:\Users\$USERNAME\Documents'), defaultextension='.*', initialfile=expandvars("$USERNAME's Public Key"), title='Save new Key...', filetypes=(fileTypes[7], fileTypes[4]))
    if publickeyPath:
        privateKeyPath = filedialog.asksaveasfilename(initialdir=expandvars(R'C:\Users\$USERNAME\Documents'), defaultextension='.*', initialfile="Private Key", title='Save new Key...', filetypes=(fileTypes[6], fileTypes[4]))
        if privateKeyPath:
            Keys = rsa.newkeys(2048)
            Keys += (Fernet.generate_key(), )
            with open(publickeyPath, 'wb') as f:
                f.write(Keys[0].save_pkcs1('PEM'))
            logger.info('User generated Public ')
            with open(privateKeyPath, 'wb') as f:
                f.write(Keys[2] + b'$' + Keys[1].save_pkcs1("PEM")) # Format: symKey$privateKey
            logger.info('User generated Private ')
            keyEntry.delete(0,'end')
            keyEntry.insert(0, privateKeyPath)
            logger.info('finished GenerateKeyPair')
        else:
            messagebox.showwarning(title='Aborted Key Generation', message=f'Key Generation aborted because you only tried to Generate One Key, but You need Both!')
            logger.info('Exited GenerateKeyPair because User only generated one Key')
    else:
        logger.info('Exited GenerateKeyPair because User generated no Keys')


def Cryptography1(mode: str, entry: Entry, PublicKeyEntry: Entry, PrivateKeyEntry: Entry, out: Entry):
    logger.info(f'Cryptography1 initiated in {mode} mode')
    try:
        if PublicKeyEntry.get() and PrivateKeyEntry.get() and entry.get():
            
            try:
                with open(PrivateKeyEntry.get(), 'rb') as f:
=======
def GenerateKeyPair(KeyFrame: Frame):
    global img1, IndicatorTooltip1, Indicator1, Indicator2, IndicatorTooltip2, img2, pubKey, privKey

    logger.info('Initiated Keypair generation')
    pubKey = filedialog.asksaveasfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), defaultextension='.*', initialfile=os.path.expandvars("$USERNAME's " + lang.Dialog['Public']), title=lang.Dialog['Save'] + lang.Dialog['Public'], filetypes=(fileTypes[8], fileTypes[4]))
    if pubKey:
        privKey = filedialog.asksaveasfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), defaultextension='.*', initialfile=lang.Dialog['Private'], title=lang.Dialog['Save'] + lang.Dialog['Private'], filetypes=(fileTypes[7], fileTypes[4]))
        if privKey:
            Keys = rsa.newkeys(2048)
            Keys += (Fernet.generate_key(), )
            with open(pubKey, 'wb') as f:
                f.write(Keys[0].save_pkcs1('PEM'))
            logger.info('User generated Public key')
            with open(privKey, 'wb') as f:
                f.write(Keys[2] + b'$' + Keys[1].save_pkcs1("PEM")) # Format: symKey$privateKey
            
            img1 = ImageTk.PhotoImage(Image.open('UI/Loaded.ico').resize((40, 40)))
            Indicator1 = Label(KeyFrame, image=img1) # LoadIndicator
            Indicator1.grid(row=1, column=1, padx=5)
            IndicatorTooltip1 = ToolTip(Indicator1, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['Loaded'], delay=1.0) # Tooltip for LoadIndicator
            img2 = ImageTk.PhotoImage(Image.open('UI/Loaded.ico').resize((40, 40)))
            Indicator2 = Label(KeyFrame, image=img2) # LoadIndicator
            Indicator2.grid(row=4, column=1, padx=5)
            IndicatorTooltip2 = ToolTip(Indicator2, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['Loaded'], delay=1.0) # Tooltip for LoadIndicator
            logger.info('finished Keypair generation')
        else:
            messagebox.showwarning(title=lang.Messages['AbortedKeyTitle'], message=lang.Messages['AbortedKeyMessage'])
            logger.info('Exited Keypair generation because User only generated one Key')
    else:
        logger.info('Exited Keypair generation because User generated no Keys')


def Cryptography1(mode: str, entry: Entry, out: Entry):
    logger.info(f'Cryptography1 initiated in {mode} mode')
    try:
        if privKey and pubKey and entry.get():
            try:
                with open(privKey, 'rb') as f:
>>>>>>> dev
                    content = f.read().split(b'$', 1)
                    symKey = content[0]
                    privateKey = content[1]
                logger.info('Loaded Private Key')
            except FileNotFoundError:
                raise PrivKeyNotFoundError

            message = entry.get()
            logger.info('Loaded message')
            
            if mode == 'Encrypt':
                try:
<<<<<<< HEAD
                    with open(PublicKeyEntry.get(), 'rb') as f:
=======
                    with open(pubKey, 'rb') as f:
>>>>>>> dev
                        publicKey = f.read()
                    logger.info('Loaded Public Key')
                except FileNotFoundError:
                    raise PubKeyNotFoundError

                message = Fernet(symKey).encrypt(message.encode())
                symKey = rsa.encrypt(symKey, rsa.PublicKey.load_pkcs1(publicKey))
                output = base64.b64encode(symKey) + b'$' + base64.b64encode(message) # Format: symKey$message
                logger.info('Created Output')
            else:
                message = message.split('$')
                logger.info('Splitted message into List')
                symKey = Fernet(rsa.decrypt(base64.b64decode(message[0]), rsa.PrivateKey.load_pkcs1(privateKey)))
                output = symKey.decrypt(base64.b64decode(message[1].encode()))
                logger.info('Created Output')
            
            out.config(state='normal')
            out.delete(0, 'end')
            out.insert(0, output.decode())
            logger.info('Inserted output into out')
        elif entry.get() == '':
            logger.info("Finished Cryptography1 because User didn't enter a message")
<<<<<<< HEAD
            messagebox.showwarning(f'No Text to {mode} entered', f'You Need to Enter a Message Before You Try to {mode}')
        elif PublicKeyEntry.get() == '':
            logger.info("Finished Cryptography1 because User didn't enter a Public Key")
            messagebox.showwarning(f'No text to {mode} entered', f'You Need to Insert a Public Key Before You Try to {mode}')
        elif PrivateKeyEntry.get() == '':
            logger.info("Finished Cryptography1 because User didn't enter a Private Key")
            messagebox.showwarning(f'No text to {mode} entered', f'You Need to Insert a Private Key Before You Try to {mode}')
    except rsa.DecryptionError:
        messagebox.showerror(title=f'Wrong Private Key entered!', message=f'This is the wrong Private Key to {mode} this message! Use the right Key!')
        logger.exception(f'Decryption failed because of a Decryption Error in {mode} mode')
    except MemoryError:
        messagebox.showerror(title=f'{mode}ion failed', message=f"The message couldn't be {mode}ed because it was too big!")
        logger.info(f'The Memory size was too small')
    except PubKeyNotFoundError:
        messagebox.showwarning(title=f'Key not found', message=f"The Public Key You tried to Use Does Not Exist!\nPlease use an Existing Key!")
        logger.info(f"The Public Key the User tried to Use does Not Exist")
    except PrivKeyNotFoundError:
        messagebox.showwarning(title=f'Key not found', message=f"The Private Key You tried to Use Does Not Exist!\nPlease use an Existing Key!")
        logger.info(f"The Private Key the User tried to Use does Not Exist")
    except Exception:
        messagebox.showerror(title='Unknown Error', message=f'An Unknown Error occurred.\nPlease open an issue at https://github.com/jasger9000/Cryptographer and attach the log file of your current session.\nLog file: {getcwd()}/Cryptographer.log')
=======
            messagebox.showwarning(lang.Messages['NoTextTitle'].split('$')[0] + lang.Dialog[mode] + lang.Messages['NoTextTitle'].split('$')[1],lang.Messages['NoTextMessage'] + lang.Dialog[mode])
        elif pubKey == '':
            logger.info("Finished Cryptography1 because User didn't enter a Public Key")
            messagebox.showwarning(lang.Messages['NoKeyTitle'].split('$')[0] + lang.Dialog[mode] + lang.Messages['NoKeyTitle'].split('$')[1], lang.Messages['NoKeyMessage'].split('$')[0] + lang.Dialog['Public'] + lang.Messages['NoKeyMessage'].split('$')[1] + lang.Dialog[mode])
        elif privKey == '':
            logger.info("Finished Cryptography1 because User didn't enter a Private Key")
            messagebox.showwarning(lang.Messages['NoKeyTitle'].split('$')[0] + lang.Dialog[mode] + lang.Messages['NoKeyTitle'].split('$')[1], lang.Messages['NoKeyMessage'].split('$')[0] + lang.Dialog['Private'] + lang.Messages['NoKeyMessage'].split('$')[1] + lang.Dialog[mode])
    except rsa.DecryptionError:
        messagebox.showerror(title=lang.Messages['WrongKeyTitle'].split('$')[0] + lang.Dialog['Private'] + lang.Messages['WrongKeyTitle'].split('$')[1], message=lang.Messages['WrongKeyMessage'].split('$')[0] + lang.Dialog['Private'] + lang.Messages['WrongKeyMessage'].split('$')[1])
        logger.exception(f'Decryption failed because of a Decryption Error in {mode} mode')
    except PubKeyNotFoundError:
        messagebox.showwarning(title=lang.Messages['KeyNotExistTitle'], message=lang.Messages['KeyNotExistMessage'].split('$')[0] + lang.Dialog['Public'] + lang.Messages['KeyNotExistMessage'].split('$')[1])
        logger.info(f"The Public Key the User tried to Use does Not Exist")
    except PrivKeyNotFoundError:
        messagebox.showwarning(title=lang.Messages['KeyNotExistTitle'], message=lang.Messages['KeyNotExistMessage'].split('$')[0] + lang.Dialog['Private'] + lang.Messages['KeyNotExistMessage'].split('$')[1])
        logger.info(f"The Private Key the User tried to Use does Not Exist")
    except Exception:
        messagebox.showerror(title=lang.Messages['UnknownTitle'], message=lang.Messages['UnknownMessage'])
>>>>>>> dev
        logger.exception(f'Unknown error/uncaught exception in Cryptography1 - {mode} mode')
    finally:
        out.config(state='readonly')
        logger.info('Cryptography1 finished')

        
<<<<<<< HEAD
def Cryptography2(mode: str, entry: Entry, PublicKeyEntry: Entry, PrivateKeyEntry: Entry, out: Entry):
    logger.info(f'Cryptography2 initiated in {mode} mode')
    try:
        if entry.get() and PublicKeyEntry.get() and PrivateKeyEntry.get():
            filePath = entry.get()
            try:
                # Checks for user conformation if file is too big
                if getsize(filePath) >= 1073741824:
                    logger.info(f'shows askYesNoPrompt1 in Cryptography2 {mode} mode')
                    userConfirm = messagebox.askyesno(title='file too big', message=f'File larger than 1 Gigabyte will take several minutes to {mode} or will fail,\nwould you still like to proceed?')
                elif getsize(filePath) >= 100000000:
                    logger.info(f'shows askYesNoPrompt2 in Cryptography2 {mode} mode')
                    userConfirm = messagebox.askyesno(title='file too big', message=f'File larger than 100mb could take a long time to {mode},\nwould you still like to proceed?')
=======
def Cryptography2(mode: str, entry: Entry, out: Entry):
    logger.info(f'Cryptography2 initiated in {mode} mode')
    try:
        if entry.get() and pubKey and privKey:
            filePath = entry.get()
            try:
                # Checks for user conformation if file is too big
                if os.path.getsize(filePath) >= 1073741824:
                    logger.info(f'shows askYesNoPrompt1 in Cryptography2 {mode} mode')
                    userConfirm = messagebox.askyesno(title=lang.Messages['TooBigTitle'], message=lang.Messages['TooBigMessage2'].split('$')[0] + lang.Dialog[mode] + lang.Messages['TooBigMessage2'].split('$')[1])
                elif os.path.getsize(filePath) >= 100000000:
                    logger.info(f'shows askYesNoPrompt2 in Cryptography2 {mode} mode')
                    userConfirm = messagebox.askyesno(title=lang.Messages['TooBigTitle'], message=lang.Messages['TooBigMessage1'].split('$')[0] + lang.Dialog[mode] + lang.Messages['TooBigMessage1'].split('$')[1])
>>>>>>> dev
                else:
                    userConfirm = True
            except FileNotFoundError:
                raise fileNotFoundError
            if userConfirm:
                try:
<<<<<<< HEAD
                    with open(PrivateKeyEntry.get(), 'rb') as f:
=======
                    with open(privKey, 'rb') as f:
>>>>>>> dev
                        content = f.read().split(b'$', 1)
                        symKey = content[0]
                        privateKey = content[1] 
                        content is None
                    logger.info('Loaded Private Key')
                except FileNotFoundError:
                    raise PrivKeyNotFoundError
                
                with open(filePath, 'rb') as f:
                    contents = f.read()
                logger.info('Loaded File Contents')
                
                if mode == 'Encrypt':
<<<<<<< HEAD
                    extention = Path(filePath).suffix
                    output = filedialog.asksaveasfilename(initialdir=expandvars(filePath[0:filePath.rfind('/') + 1]), defaultextension='.*', initialfile=f'Encrypted {filePath[filePath.rfind("/") + 1:len(filePath.replace(extention, ""))]}', title='Save Encrypted file...', filetypes=(('Encrypted file', '*.Encrypted'),('Text file', '*.txt'),('Any file', '*.*')))
                    logger.info('got new filePath')
                    try:
                        with open(PublicKeyEntry.get(), 'rb') as f:
=======
                    extension = pathlib.Path(filePath).suffix
                    output = filedialog.asksaveasfilename(initialdir=os.path.expandvars(filePath[0:filePath.rfind('/') + 1]), defaultextension='.*', initialfile=f'Encrypted {filePath[filePath.rfind("/") + 1:len(filePath.replace(extension, ""))]}', title=lang.Dialog['Save'] + lang.Dialog['Encrypted'] + lang.Dialog['file'], filetypes=(fileTypes[5],fileTypes[0],fileTypes[4]))
                    logger.info('got new filePath')
                    try:
                        with open(pubKey, 'rb') as f:
>>>>>>> dev
                            publicKey = f.read()
                        logger.info('Loaded Public Key')
                    except FileNotFoundError:
                        raise PubKeyNotFoundError
                    
                    contents = Fernet(symKey).encrypt(contents)
                    symKey = rsa.encrypt(symKey, rsa.PublicKey.load_pkcs1(publicKey))
<<<<<<< HEAD
                    contents = base64.b64encode(extention.encode()) + b'$' + base64.b64encode(symKey) + b'$' + base64.b64encode(contents) # Format: extention$symKey$contents
=======
                    contents = base64.b64encode(extension.encode()) + b'$' + base64.b64encode(symKey) + b'$' + base64.b64encode(contents) # Format: extension$symKey$contents
>>>>>>> dev
                    with open(output, 'wb') as f:
                        f.write(contents)
                    logger.info('Created contents and saved them to filePath')
                else:
                    contents = contents.split(b'$')
                    logger.info('Splitted file into List')
                    symKey = Fernet(rsa.decrypt(base64.b64decode(contents[1]), rsa.PrivateKey.load_pkcs1(privateKey)))
                    contents[2] = symKey.decrypt(base64.b64decode(contents[2])).decode()
                    logger.info('Decrypted Contents')

<<<<<<< HEAD
                    output = filedialog.asksaveasfilename(initialdir=expandvars(filePath[0:filePath.rfind('/') + 1]), defaultextension='.*', initialfile=filePath[filePath.rfind("/") + 1:len(filePath.replace(Path(filePath).suffix, ''))], title='Save Decrypted file...', filetypes=(('Decrypted file',f'*{base64.b64decode(contents[0]).decode()}' ),('Any file', '*.*')))
=======
                    output = filedialog.asksaveasfilename(initialdir=os.path.expandvars(filePath[0:filePath.rfind('/') + 1]), defaultextension='.*', initialfile=filePath[filePath.rfind("/") + 1:len(filePath.replace(pathlib.Path(filePath).suffix, ''))], title=lang.Dialog['Save'] + lang.Dialog['Decrypted'] + lang.Dialog['file'], filetypes=((lang.Dialog['Decrypted'] + lang.Dialog['file'],f'*{base64.b64decode(contents[0]).decode()}' ),fileTypes[4]))
>>>>>>> dev
                    logger.info('Got New filePath')
                    with open(output, 'w') as f:
                        f.write(contents[2])
                    logger.info('Saved Contents to filePath')

                out.config(state='normal')
                out.delete(0, 'end')
                out.insert(0, output)
                logger.info('Inserted output into out')
        elif entry.get() == '':
<<<<<<< HEAD
            logger.info("Finished Cryptography2 because User didn't enter a filePath")
            messagebox.showwarning(f'No File to {mode} entered', f'You Need to Enter a File Path Before You Try to {mode}')
        elif PublicKeyEntry.get() == '':
            logger.info("Finished Cryptography2 because User didn't enter a Public Key")
            messagebox.showwarning(f'No text to {mode} entered', f'You Need to Insert a Public Key Before You Try to {mode}')
        elif PrivateKeyEntry.get() == '':
            logger.info("Finished Cryptography2 because User didn't enter a Private Key")
            messagebox.showwarning(f'No text to {mode} entered', f'You Need to Insert a Private Key Before You Try to {mode}')
    except ValueError:
        messagebox.showerror(title=f'{mode}ion failed', message=f"The file couldn't be {mode}ed because the file type is not supported!")
        logger.exception(f"Showed ValueError")
    except rsa.DecryptionError:
        messagebox.showerror(title=f'Wrong Private Key entered!', message=f'This is the wrong Private Key to {mode} this message! Use the right Key!')
        logger.exception(f'Decryption failed because of a Decryption Error in {mode} mode')
    except MemoryError:
        messagebox.showerror(title=f'{mode}ion failed', message=f"The message couldn't be {mode}ed because it was too big!")
        logger.info(f'The Memory size was too small')
    except fileNotFoundError:
        messagebox.showwarning(title='File not found', message=f'The File you would Like to {mode} was not Found!\nPlease Use an Existing File!')
        logger.info(f"The File The User Tried To Use didn't Exist")
    except PubKeyNotFoundError:
        messagebox.showwarning(title=f'Key not found', message=f"The Public Key You tried to Use Does Not Exist!\nPlease use an Existing Key!")
        logger.info(f"The Public Key the User tried to Use does Not Exist")
    except PrivKeyNotFoundError:
        messagebox.showwarning(title=f'Key not found', message=f"The Private Key You tried to Use Does Not Exist!\nPlease use an Existing Key!")
        logger.info(f"The Private Key the User tried to Use does Not Exist")
    except Exception:
        messagebox.showerror(title='Unknown Error', message=f'An Unknown Error occurred.\nPlease open an issue at https://github.com/jasger9000/Cryptographer and attach the log file of your current session.\nLog file: {getcwd()}/Cryptographer.log')
=======
            logger.info("Finished Cryptography2 because User didn't enter a message")
            messagebox.showwarning(lang.Messages['NoTextTitle'].split('$')[0] + lang.Dialog[mode] + lang.Messages['NoTextTitle'].split('$')[1],lang.Messages['NoTextMessage'] + lang.Dialog[mode])
        elif pubKey == '':
            logger.info("Finished Cryptography2 because User didn't enter a Public Key")
            messagebox.showwarning(lang.Messages['NoKeyTitle'].split('$')[0] + lang.Dialog['Public'] + lang.Messages['NoKeyTitle'].split('$')[1], lang.Messages['NoKeyMessage'].split('$')[0] + lang.Dialog['Public'] + lang.Messages['NoKeyMessage'].split('$')[1] + lang.Dialog[mode])
        elif privKey == '':
            logger.info("Finished Cryptography2 because User didn't enter a Private Key")
            messagebox.showwarning(lang.Messages['NoKeyTitle'].split('$')[0] + lang.Dialog['Private'] + lang.Messages['NoKeyTitle'].split('$')[1], lang.Messages['NoKeyMessage'].split('$')[0] + lang.Dialog['Private'] + lang.Messages['NoKeyMessage'].split('$')[1] + lang.Dialog[mode])
    except ValueError:
        messagebox.showerror(title=lang.Dialog[f'{mode}ion'] + lang.Messages['ValueTitle'], message=lang.Dialog[f'{mode}ion'] + lang.Messages['ValueMessage'])
        logger.exception(f"Showed ValueError")
    except fileNotFoundError:
        messagebox.showwarning(title=lang.Messages['fileNotFoundTitle'], message=lang.Messages['fileNotFoundMessage'])
        logger.info(f"The File The User Tried To Use didn't Exist")
    except rsa.DecryptionError:
        messagebox.showerror(title=lang.Messages['WrongKeyTitle'].split('$')[0] + lang.Dialog['Private'] + lang.Messages['WrongKeyTitle'].split('$')[1], message=lang.Messages['WrongKeyMessage'].split('$')[0] + lang.Dialog['Private'] + lang.Messages['WrongKeyMessage'].split('$')[1])
        logger.exception(f'Decryption failed because of a Decryption Error in {mode} mode')
    except MemoryError:
        messagebox.showerror(title=lang.Dialog[f'{mode}ion'] + lang.Messages['TooBigTitle'], message=lang.Messages['TooBigMessage'].split('$')[0] + lang.Dialog[f'{mode}ed'] + lang.Messages['TooBigMessage'].split('$')[1])
        logger.info(f'{mode}ion failed, file was too big')
    except PubKeyNotFoundError:
        messagebox.showwarning(title=lang.Messages['KeyNotExistTitle'], message=lang.Messages['KeyNotExistMessage'].split('$')[0] + lang.Dialog['Public'] + lang.Messages['KeyNotExistMessage'].split('$')[1])
        logger.info(f"The Public Key the User tried to Use does Not Exist")
    except PrivKeyNotFoundError:
        messagebox.showwarning(title=lang.Messages['KeyNotExistTitle'], message=lang.Messages['KeyNotExistMessage'].split('$')[0] + lang.Dialog['Private'] + lang.Messages['KeyNotExistMessage'].split('$')[1])
        logger.info(f"The Private Key the User tried to Use does Not Exist")
    except Exception:
        messagebox.showerror(title=lang.Messages['UnknownTitle'], message=lang.Messages['UnknownMessage'])
>>>>>>> dev
        logger.exception(f'Unknown error/uncaught exception in Cryptography2 - {mode} mode')
    finally:
        out.config(state='readonly')
        logger.info('Cryptography2 finished')
    
<<<<<<< HEAD
def Copy(root: Tk, out: Entry):
    logger.info('Copy function initiated')
    try:
        root.clipboard_clear()
        root.clipboard_append(out.get())
    except Exception:
        logger.exception(f'Unknown error/uncaught exception in Copy function')
        messagebox.showerror(title='Unknown error', message=f'An Unknown Error occurred.\nPlease open an issue at https://github.com/jasger9000/Cryptographer and attach the log file of your current session.\nLog file: {getcwd()}/Cryptographer.log')
    finally:
        logger.info('Copy function finished')

def Delete(out: Entry):
    logger.info('Delete function initiated')
    try:
        out.config(state='normal')
        out.delete(0, 'end')
    except Exception:
        logger.exception(f'Unknown/uncaught exception in Delete function')
        messagebox.showerror(title='Unknown Error', message=f'An Unknown Error occurred.\nPlease open an issue at https://github.com/jasger9000/Cryptographer and attach the log file of your current session.\nLog file: {getcwd()}/Cryptographer.log')
    finally:
        out.config(state='readonly')
        logger.info('Delete function finished')

def main(root: Tk, version: str):
    # GUI Configuration
    root.title(f'Asymmetric Cryptographer ver. {version}')
    root.geometry('')
    TitleLabel = Label(root, text='Asymmetric Cryptographer', font=('Helvetica', 14, BOLD, UNDERLINE))
    TitleLabel.grid(row=0, column=0, columnspan=2)
    logger.info('loaded Tk Config')
    
    # Keys Frame
    frame0 = LabelFrame(root, text='Keys', font=('Arial', 12), padx=10, pady=6)
    frame0.grid(row=1, column=0, padx=10, columnspan=2)

    # Public Key Input
    Label(frame0, text='Public Key:', font=('Arial', 12, UNDERLINE)).grid(row=0, column=0, columnspan=2)
    Button(frame0, text='Browse', command=lambda: BrowseKeyDialog(publicKeyEntry, 'Public')).grid(row=1, column=0)
    publicKeyEntry = Entry(frame0, width=25, font=('Arial', 14))
    publicKeyEntry.grid(row=1, column=1)
    logger.info('loaded PublicKey input') # Section Loaded
    
    Button(frame0, text='Generate Key Pair', command=lambda: GenerateKeyPair(PrivateKeyEntry)).grid(row=1, column=2)

    # Private Key Input
    Label(frame0, text='Private Key:',font=('Arial', 12, UNDERLINE)).grid(row=0, column=3, columnspan=2)
    PrivateKeyEntry = Entry(frame0, width=25, font=('Arial', 14))
    PrivateKeyEntry.grid(row=1, column=3)
    Button(frame0, text='Browse', command=lambda: BrowseKeyDialog(PrivateKeyEntry, 'Private')).grid(row=1, column=4)
    logger.info('loaded PrivateKey input') # Section Loaded


    # Encryption Frame
    frame1 = LabelFrame(root, text='Encrypt', font=('Arial', 12), padx=10, pady=12)
    frame1.grid(row=2, column=0, padx=10, pady=10)

    # Encrypt option 1
    Label(frame1, text='Encrypt a message:').grid(row=0, column=0)
    Encrypt1Entry = Entry(frame1, font=('Arial', 14), width=20)
    Encrypt1Entry.grid(row=1, column=0)
    Button(frame1, text='Encrypt', command=lambda: Cryptography1('Encrypt', Encrypt1Entry, publicKeyEntry, PrivateKeyEntry, out)).grid(row=1, column=1)

    # Encrypt option 2
    Label(frame1, text='\nEncrypt a file:').grid(row=2, column=0)
    Encrypt2Entry = Entry(frame1, font=('Arial', 14), width=20)
    Encrypt2Entry.grid(row=3, column=0)
    Button(frame1, text='Encrypt', command=lambda: Cryptography2('Encrypt', Encrypt2Entry, publicKeyEntry, PrivateKeyEntry, out)).grid(row=3,column=1)
    Button(frame1, text='Browse', command=lambda: BrowseEncryptDialog(Encrypt2Entry)).grid(row=3, column=2) 
    logger.info('loaded encrypt options') # Section Loaded


    # Decryption Frame
    frame2 = LabelFrame(root, text='Decrypt', font=('Arial', 12), padx=10, pady=12)
    frame2.grid(row=2, column=1, padx=10, pady=10)

    # Decrypt option 1
    Label(frame2, text='Decrypt a message:').grid(row=0, column=0)
    Decrypt1Entry = Entry(frame2, font=('Arial', 14), width=20)
    Decrypt1Entry.grid(row=1, column=0)
    Button(frame2, text='Decrypt', command=lambda: Cryptography1('Decrypt', Decrypt1Entry, publicKeyEntry, PrivateKeyEntry, out)).grid(row=1, column=1)

    # Decrypt option 2
    Label(frame2, text='\nDecrypt a file:').grid(row=2, column=0)
    Decrypt2Entry = Entry(frame2, font=('Arial', 14), width=20)
    Decrypt2Entry.grid(row=3, column=0)
    Button(frame2, text='Decrypt', command=lambda: Cryptography2('Decrypt', Decrypt2Entry, publicKeyEntry, PrivateKeyEntry, out)).grid(row=3,column=1)
    Button(frame2, text='Browse', command=lambda: BrowseDecryptDialog(Decrypt2Entry)).grid(row=3, column=2)
    logger.info('loaded decrypt options') # Section Loaded

    # Output
    frame3 = LabelFrame(root, text='Output:', font=('Arial', 12, UNDERLINE), padx=10, pady=12, borderwidth=0)
    frame3.grid(row=3, column=0, padx=10, columnspan=2)

    Button(frame3, text='Delete', command= lambda: Delete(out)).grid(row=0, column=0)
    out = Entry(frame3, font=('Arial', 14), width=27, state='readonly')
    out.grid(row=0, column=1)
    Button(frame3, text='Copy', command=lambda: Copy(root, out)).grid(row=0, column=2)

    return frame0, frame1, frame2, frame3, TitleLabel

def Unload(frame0: LabelFrame,frame1: LabelFrame,frame2: LabelFrame,frame3: LabelFrame, TitleLabel: Label):
    frame0.destroy()
    frame1.destroy()
    frame2.destroy()
    frame3.destroy()
    TitleLabel.destroy()

=======

def Window(EncryptFrame: Frame, DecryptFrame: Frame, KeyFrame: LabelFrame, out: Entry, l: str):
    global fileTypes, lang, privKey, pubKey, Indicator1, IndicatorTooltip1, img1, Indicator2, IndicatorTooltip2, img2
    from Cryptographer import LoadFileTypes, LoadLang
    
    # Lang Configuration
    lang = LoadLang(l)
    fileTypes = LoadFileTypes(lang)
    
    # Public Key Input
    pubKey = ''
    Label(KeyFrame, text=lang.AsymMain['PublicKeyTitle'], font=('Arial', 12, UNDERLINE)).grid(row=0, column=0, columnspan=2)
    Button(KeyFrame, text=lang.Main['BrowseBtn'], command=lambda: BrowseKeyDialog('Public', KeyFrame)).grid(row=1, column=0)
    if pubKey == '':
        img1 = ImageTk.PhotoImage(Image.open('UI/NotLoaded.ico').resize((40, 40)))
    else:
        img1 = ImageTk.PhotoImage(Image.open('UI/Loaded.ico').resize((40, 40)))
    Indicator1 = Label(KeyFrame, image=img1) # LoadIndicator
    Indicator1.grid(row=1, column=1, padx=5)
    IndicatorTooltip1 = ToolTip(Indicator1, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['NotLoaded'], delay=1.0) # Tooltip for LoadIndicator
    logger.info('loaded PublicKey input') # Section Loaded
    
    Button(KeyFrame, text=lang.AsymMain['GenerateKeyBtn'], command=lambda: GenerateKeyPair(KeyFrame)).grid(row=2, column=0, pady=10)

    # Private Key Input
    privKey = ''
    Label(KeyFrame, text=lang.AsymMain['PrivateKeyTitle'],font=('Arial', 12, UNDERLINE)).grid(row=3, column=0, columnspan=2)
    Button(KeyFrame, text=lang.Main['BrowseBtn'], command=lambda: BrowseKeyDialog('Private', KeyFrame)).grid(row=4, column=0)
    if privKey == '':
        img2 = ImageTk.PhotoImage(Image.open('UI/NotLoaded.ico').resize((40, 40)))
    else:
        img2 = ImageTk.PhotoImage(Image.open('UI/Loaded.ico').resize((40, 40)))
    Indicator2 = Label(KeyFrame, image=img2) # LoadIndicator
    Indicator2.grid(row=4, column=1, padx=5)
    IndicatorTooltip2 = ToolTip(Indicator2, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['NotLoaded'], delay=1.0) # Tooltip for LoadIndicator
    logger.info('loaded PrivateKey input') # Section Loaded


    # Encrypt option 1
    Label(EncryptFrame, text=lang.Main['Encrypt1Title']).grid(row=0, column=0)
    Encrypt1Entry = Entry(EncryptFrame, width=40) # Define Entry
    Encrypt1Entry.grid(row=1, column=0, padx=5) # Put Entry on screen
    Button(EncryptFrame, text=lang.Main['Encrypt'], command=lambda: Cryptography1('Encrypt', Encrypt1Entry, out)).grid(row=1, column=1)

    # Encrypt option 2
    Label(EncryptFrame, text=lang.Main['Encrypt2Title']).grid(row=2, column=0)
    Encrypt2Entry = Entry(EncryptFrame, width=40)
    Encrypt2Entry.grid(row=3, column=0, padx=5)
    Button(EncryptFrame, text=lang.Main['Encrypt'], command=lambda: Cryptography2('Encrypt', Encrypt2Entry, out)).grid(row=3,column=1)
    Button(EncryptFrame, text=lang.Main['BrowseBtn'], command=lambda: BrowseEncryptDialog(Encrypt2Entry)).grid(row=3, column=2) 
    logger.info('loaded encrypt options') # Section Loaded


    # Decrypt option 1
    Label(DecryptFrame, text=lang.Main['Decrypt1Title']).grid(row=0, column=0)
    Decrypt1Entry = Entry(DecryptFrame, width=40)
    Decrypt1Entry.grid(row=1, column=0, padx=5)
    Button(DecryptFrame, text=lang.Main['Decrypt'], command=lambda: Cryptography1('Decrypt', Decrypt1Entry, out)).grid(row=1, column=1)

    # Decrypt option 2
    Label(DecryptFrame, text=lang.Main['Decrypt2Title']).grid(row=2, column=0)
    Decrypt2Entry = Entry(DecryptFrame, width=40)
    Decrypt2Entry.grid(row=3, column=0, padx=5)
    Button(DecryptFrame, text=lang.Main['Decrypt'], command=lambda: Cryptography2('Decrypt', Decrypt2Entry, out)).grid(row=3,column=1)
    Button(DecryptFrame, text=lang.Main['BrowseBtn'], command=lambda: BrowseDecryptDialog(Decrypt2Entry)).grid(row=3, column=2)
    logger.info('loaded decrypt options') # Section Loaded
>>>>>>> dev
