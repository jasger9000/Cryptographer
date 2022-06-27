<<<<<<< HEAD
from tkinter import UNDERLINE, filedialog, messagebox, Tk, Label, Button, Entry, LabelFrame
from tkinter.font import BOLD
from cryptography.fernet import Fernet, InvalidToken
from pathlib import Path
import logging
from os.path import expandvars, getsize
from os import getcwd

# TODO Make User send log to me
=======
import base64
from tkinter import filedialog, messagebox
from tktooltip import ToolTip 
from PIL import ImageTk, Image
from tkinter.ttk import Button, Entry, Frame, Label
from cryptography.fernet import Fernet, InvalidToken
from pathlib import Path
import logging
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
<<<<<<< HEAD
debug = True
if debug is True:
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(fmt)
    streamHandler.setLevel(logging.DEBUG)
    logger.addHandler(streamHandler)


textFiles = '*.txt', '*.doc', '*.docx', '*.log', '*.msg', '*.odt', '*.pages', '*.rtf', '*.tex', '*.wpd', '*.wps'
videoFiles = '*.mp4', '*.mov', '*.avi', '*.flv', '*.mkv', '*.wmv', '*.avchd', '*.webm', '*MPEG-4', '*.H.264'
audioFiles = '*.aif', '*.aiff', '*.iff', '*.m3u', '*.m4a', '*.mp3', '*.mpa', '*.wav', '*.wma', '*.aup3', '*.aup', '*.ogg', '*.mp2'
pictureFiles = '*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp', '*.raw', '*.tiff', '*.psd', '*.cr2'


def BrowseKeyDialog(keyEntry):
    browseKeyDialog = filedialog.askopenfilename(initialdir=expandvars(R'C:\Users\$USERNAME\Documents'), title='Open Key...', filetypes=(('Key files', '*.key'),('All files', '*.*')))
    if browseKeyDialog:
        logger.info('User selected key')
        keyEntry.delete(0,"end")
        keyEntry.insert(0, browseKeyDialog)
    return

def BrowseEncryptDialog(encrypt2Entry):
    global textFiles
    browseEncryptDialog = filedialog.askopenfilename(initialdir=expandvars(R'C:\Users\$USERNAME\Documents'), title=f'Select file to Encrypt...', filetypes=(('Text files', textFiles), ('Video files', videoFiles), ('Audio files', audioFiles),('Picture files', pictureFiles), ('Pdf files', '*.pdf'), ('All files', '*.*')))
=======
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(fmt)
streamHandler.setLevel(logging.DEBUG)
logger.addHandler(streamHandler)


class fileNotFoundError(FileNotFoundError):
    pass
class KeyNotFoundError(FileNotFoundError):
    pass


def BrowseKeyDialog(KeyFrame):
    global key, img, IndicatorTooltip, Indicator
    key = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=lang.Dialog['Open'] + lang.Dialog['Key'], filetypes=(fileTypes[6], fileTypes[4]))
    if key != '':
        img = ImageTk.PhotoImage(Image.open('UI/Loaded.ico').resize((40, 40)))
        Indicator = Label(KeyFrame, image=img) # LoadIndicator
        Indicator.grid(row=0, column=1, rowspan=2, padx=5)
        IndicatorTooltip = ToolTip(Indicator, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['Loaded'], delay=1.0) # Tooltip for LoadIndicator
        

def BrowseEncryptDialog(encrypt2Entry: Entry):
    browseEncryptDialog = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=lang.Dialog['Open'] + lang.Dialog['file'] + lang.Dialog['Encrypt'], filetypes=(fileTypes[0], fileTypes[1], fileTypes[2], fileTypes[3], fileTypes[4]))
>>>>>>> dev
    if browseEncryptDialog:
        logger.info('User selected file to Encrypt')
        encrypt2Entry.delete(0,"end")
        encrypt2Entry.insert(0, browseEncryptDialog)
<<<<<<< HEAD
    return

def BrowseDecryptDialog(decrypt2Entry):
    browseDecryptDialog = filedialog.askopenfilename(initialdir=expandvars(R'C:\Users\$USERNAME\Documents'), title=f'Select file to Decrypt...', filetypes=(('Encrypted Files', '*.Encrypted'), ('Text files', textFiles), ('All files', '*.*')))
    if browseDecryptDialog:
        logger.info('User selected file to Decrypt')
        decrypt2Entry.delete(0,"end")
        decrypt2Entry.insert(0, browseDecryptDialog)
    return 

def GenerateKey(keyEntry):
    keyPath = filedialog.asksaveasfilename(initialdir=expandvars(R'C:\Users\$USERNAME\Documents'), defaultextension='.*', initialfile='Key', title='Save new Key...', filetypes=(('Key files', '*.key'),('All files', '*.*')))
    if keyPath:
        logger.info('User generated key')
        keyEntry.delete(0,"end")
        keyEntry.insert(0, keyPath)
        with open(keyPath, 'wb') as f:
            f.write(Fernet.generate_key())
    return

def Cryptography1(mode: str, entry, keyEntry, out):
    logger.info(f'Cryptography1 initiated in {mode} mode')
    keyPath = keyEntry.get()
    if len(keyPath) != 0 and len(entry.get()) != 0:
        try:
            logger.info(f'imports key for Cryptography1 - {mode} mode')
            with open(keyPath, 'rb') as f:
                k = Fernet(f.read())  # Imports the key
        except FileNotFoundError:
            logger.info(f'shows KeyNotFound warning to user in Cryptography1 - {mode} mode')
            messagebox.showwarning(title='Key not found', message=f'The {mode}ion Key you tried to use does not exist!\nPlease use an existing Key!')
        except Exception:
            logger.exception(f'Unknown error/uncaught exception in Cryptography1 - {mode} mode')
            messagebox.showerror(title='Unknown error', message=f'An unknown error occurred while trying to {mode}!')
        else:
            
            encoded = entry.get().encode()  # Encodes the message
            try:
                if mode == 'Encrypt':
                    logger.info(f'Encrypted a message')
                    message = k.encrypt(encoded)  # Encrypts the message
                elif mode == 'Decrypt':
                    logger.info(f'Decrypted a message')
                    message = k.decrypt(encoded) # Decrypts the message
            except InvalidToken:
                logger.info(f'shows InvalidToken warning to user in Cryptography1 - {mode} mode')
                messagebox.showerror(title=f'Wrong {mode}ion Key entered!', message=f'This is the wrong Key to {mode} this message! Use the right Key to {mode}!')
            except Exception:
                logger.exception(f'Unknown error/uncaught exception in Cryptography1 - {mode} mode')
                messagebox.showerror(title='Unknown error', message=f'An unknown error occurred while trying to {mode}!')
            else:
                # deletes entry and encoded Contents
                encoded = None
                entry.delete(0, 'end')

                # Writes the message
                out.config(state='normal')
                out.delete(0, 'end')
                out.insert(0, message)
                out.config(state='readonly')
                logger.info('Finished Cryptography1 function')
    elif len(keyPath) == 0:
        logger.info(f'shows NoKeyEntered warning in Cryptograph1 {mode} mode')
        messagebox.showwarning(title=f'No {mode}ion Key entered', message=f'Please insert or generate a {mode}ion Key to {mode} the message with!')
    elif len(entry.get()) == 0:
        logger.info(f'shows NoMessageEntered warning in Cryptography1 {mode} mode')
        messagebox.showwarning(title=f'No message to {mode} entered', message=f'Please enter a message to {mode} before you try to {mode} it!')
    return

def Cryptography2(mode: str, entry, keyEntry, out):
    logger.info(f'Cryptography2 initiated in {mode} mode')
    # get variables
    filePath = entry.get()

    
    keyPath = keyEntry.get()
    if len(keyPath) != 0 and len(filePath) != 0:
        try:
            # Checks for user conformation if file is too big
            if getsize(filePath) >= 1073741824:
                logger.info(f'shows askYesNoPrompt1 in Cryptography2 {mode} mode')
                userConfirm = messagebox.askyesno(title='file too big', message=f'File larger than 1 Gigabyte will take several minutes to {mode} or will fail,\nwould you still like to proceed?')
            elif getsize(filePath) >= 100000000:
                logger.info(f'shows askYesNoPrompt2 in Cryptography2 {mode} mode')
                userConfirm = messagebox.askyesno(title='file too big', message=f'File larger than 100mb could take a long time to {mode},\nwould you still like to proceed?')
            else:
                userConfirm = True
        except FileNotFoundError:
            #shows error if file was not found
            logger.info(f'shows FileNotFound warning in Cryptography2 {mode} mode')
            messagebox.showwarning(title='File not found', message=f'The file you would like to {mode} was not found!\nPlease use an existing file!')
        except Exception:
            logger.exception(f'Unknown error/uncaught exception in Cryptography2 - {mode} mode')
            messagebox.showerror(title='Unknown error', message=f'An unknown error occurred while trying to {mode}!')
        else:
            if userConfirm:
                try:
                    logger.info(f'imports key in Cryptography2 {mode} mode')
                    # imports encryption Key
                    with open(keyPath, 'rb') as f:
                        k = Fernet(f.read())  # Imports the Key
                    
                    # CheckSeperator
                    if filePath.find('/') != -1:
                        seperator = '/'
                    elif filePath.find(chr(92)) != -1:
                        seperator = chr(92)

                    # imports fileContents of file to encrypt
                    logger.info(f'imports fileContents in Cryptography2 {mode} mode')
                    with open(filePath, 'rb') as f:
                        fileContents = f.read()

                    # Encrypts or Decrypts the file, creates filePath2 + some other variables and deletes fileContents and filePath out of Memory
                    if mode == 'Encrypt':
                        fileContents = k.encrypt(fileContents)
                        fileExtention = Path(filePath).suffix
                        pathLength2 = len(filePath.replace(fileExtention, ''))
                        filePath2 = filedialog.asksaveasfilename(initialdir=expandvars(filePath[0:filePath.rfind(seperator) + 1]), defaultextension='.*', initialfile=f'Encrypted {filePath[filePath.rfind(seperator) + 1:pathLength2]}', title='Save Encrypted file...', filetypes=(('Encrypted file', '*.Encrypted'),('Text file', '*.txt'),('Any file', '*.*')))
                        # writes encrypted Contents to file
                        if filePath2:
                            logger.info('Encrypts and saves file')
                            with open(filePath2, 'wb') as f:
                                f.write(fileExtention.encode()+ '$'.encode() +fileContents)
                        else:
                            logger.info('Finished Cryptography2 because User cancelled saving')
                            return
                    elif mode == 'Decrypt':
                        fileContents = fileContents.decode().split('$', 1)
                        extention = fileContents[0]
                        fileContents = k.decrypt(fileContents[1].encode())
                        pathLength2 = len(filePath.replace(Path(filePath).suffix, ''))
                        filePath2 = filedialog.asksaveasfilename(initialdir=expandvars(filePath[0:filePath.rfind(seperator) + 1]), defaultextension='.*', initialfile=filePath[filePath.rfind(seperator) + 1:pathLength2], title='Save Decrypted file...', filetypes=(('Decrypted file',f'*{extention}' ),('Any file', '*.*')))
                        if filePath2:
                            logger.info('Decrypts and saves file')
                            with open(filePath2, 'wb') as f:
                                f.write(fileContents)
                        else:
                            logger.info('Finished Cryptography2 because User cancelled saving')
                            return

                    
                    # writes filePath2 to out
                    out.config(state='normal')
                    out.delete(0, 'end')
                    out.insert(0, filePath2)
                    out.config(state='readonly')
                    logger.info(f'finished Cryptography2 in {mode} mode')
                except ValueError:
                    logger.info(f'shows ValueError error in Cryptography2 in {mode} mode')
                    messagebox.showerror(title=f'{mode}ion failed', message=f"The file couldn't be {mode}ed because the file type is not supported!")
                except InvalidToken:
                    logger.info(f'shows InvalidToken warning in Cryptography2 in {mode} mode')
                    messagebox.showerror(title=f'Wrong {mode}ion Key entered!', message=f'This is the wrong Key to {mode} this message! Use the right Key to {mode}!')
                except MemoryError:
                    logger.info(f'shows MemoryError error in Cryptography2 in {mode} mode')
                    messagebox.showerror(title=f'{mode}ion failed', message=f"The file couldn't be {mode}ed because it was too big!")
                except FileNotFoundError:
                    logger.info(f'shows KeyNotFound warning in Cryptography2 {mode} mode')
                    messagebox.showwarning(title=f'{mode}ion Key not found', message=f'The {mode}ion Key you tried to use does not exist!\nPlease use an existing Key!')
                except Exception:
                    logger.exception(f'Unknown error/uncaught exception in Cryptography2 - {mode} mode')
                    messagebox.showerror(title='Unknown error', message=f'An unknown error occurred while trying to {mode}!')
            else:
                logger.info('Finished Cryptography2 because UserConfirm is False')    
    elif len(keyPath) == 0:
        logger.info(f'shows NoKeyEntered warning in Cryptography2 {mode} mode')
        messagebox.showwarning(title=f'No {mode}ion Key entered', message=f'Please insert or generate a {mode}ion Key to {mode} the file with!')
    elif len(filePath) == 0:
        logger.info(f'shows NoMessageEntered warning in Cryptography2 {mode} mode')
        messagebox.showwarning(title='No filepath entered', message=f'Please enter a filepath of the file to {mode}!')
    return

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
    root.title(f'Symmetric Cryptographer ver. {version}')
    root.geometry('')
    TitleLabel = Label(root, text='Symmetric Cryptographer', font=('Helvetica', 14, BOLD, UNDERLINE))
    TitleLabel.grid(row=0, column=0, columnspan=2)
    logger.info('loaded Tk Config')

    # Key Frame
    frame0 = LabelFrame(root, text='En-/Decryption Key:', font=('Arial', 12, UNDERLINE), padx=120, pady=12)
    frame0.grid(row=1, column=0, padx=10, columnspan=2)

    # Key Input
    Button(frame0, text='Generate Key', command=lambda: GenerateKey(KeyEntry)).grid(row=0, column=0)
    KeyEntry = Entry(frame0, width=25, font=('Arial', 14))
    KeyEntry.grid(row=0, column=1)
    Button(frame0, text='Browse', command=lambda: BrowseKeyDialog(KeyEntry)).grid(row=0, column=2)

    # Encryption Frame
    frame1 = LabelFrame(root, text='Encrypt', font=('Arial', 12), padx=10, pady=12)
    frame1.grid(row=2, column=0, padx=10, pady=10)

    # Encrypt option 1
    Label(frame1, text='Encrypt a message:').grid(row=0, column=0) # Description Label
    encrypt1Entry = Entry(frame1, font=('Arial', 14), width=20) # Define Entry
    encrypt1Entry.grid(row=1, column=0) # Put Entry on screen
    Button(frame1, text='Encrypt', command=lambda: Cryptography1('Encrypt', encrypt1Entry, KeyEntry, out)).grid(row=1, column=1) # Encrypt Btn

    # Encrypt option 2
    Label(frame1, text='\n\nEncrypt a file:').grid(row=2, column=0) # Description Label
    encrypt2Entry = Entry(frame1, font=('Arial', 14), width=20) # Define Entry
    encrypt2Entry.grid(row=3, column=0) # Put Entry on screen
    Button(frame1, text='Encrypt', command=lambda: Cryptography2('Encrypt', encrypt2Entry, KeyEntry, out)).grid(row=3,column=1) # Encrypt Btn
    Button(frame1, text='Browse', command=lambda: BrowseEncryptDialog(encrypt2Entry)).grid(row=3, column=2) # BrowseCryptographyDialog
    logger.info('loaded encrypt options')

    # Decryption Frame
    frame2 = LabelFrame(root, text='Decrypt', font=('Arial', 12), padx=10, pady=12)
    frame2.grid(row=2, column=1, padx=10, pady=10)

    # Decrypt option 1
    Label(frame2, text='Decrypt a message:').grid(row=0, column=0) # Description Label
    decrypt1Entry = Entry(frame2, font=('Arial', 14), width=20) # Define Entry
    decrypt1Entry.grid(row=1, column=0) # Put Entry on screen
    Button(frame2, text='Decrypt', command=lambda: Cryptography1('Decrypt', decrypt1Entry, KeyEntry, out)).grid(row=1, column=1) # Decrypt Btn

    # Decrypt option 2
    Label(frame2, text='\n\nDecrypt a file:').grid(row=2, column=0) # Description Label
    decrypt2Entry = Entry(frame2, font=('Arial', 14), width=20) # Define Entry
    decrypt2Entry.grid(row=3, column=0) # Put Entry on screen
    Button(frame2, text='Decrypt', command=lambda: Cryptography2('Decrypt', decrypt2Entry, KeyEntry, out)).grid(row=3,column=1) # Decrypt Btn
    Button(frame2, text='Browse', command=lambda: BrowseDecryptDialog(decrypt2Entry)).grid(row=3, column=2) # BrowseDecryptDialog
    logger.info('loaded decrypt options')

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

def BrowseDecryptDialog(decrypt2Entry: Entry):
    browseDecryptDialog = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=lang.Dialog['Open'] + lang.Dialog['file'] + lang.Dialog['Decrypt'], filetypes=(fileTypes[5], fileTypes[0]))
    if browseDecryptDialog:
        logger.info('User selected file to Decrypt')
        decrypt2Entry.delete(0,"end")
        decrypt2Entry.insert(0, browseDecryptDialog) 

def GenerateKey():
    global key

    keyPath = filedialog.asksaveasfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), defaultextension='.*', initialfile=lang.Dialog['Key'], title=lang.Dialog['Save'] + lang.Dialog['Key'], filetypes=(fileTypes[6], fileTypes[4]))
    if keyPath:
        logger.info('User generated key')
        with open(keyPath, 'wb') as f:
            f.write(Fernet.generate_key())
        key = keyPath

def Cryptography1(mode: str, entry: Entry, out: Entry):
    logger.info(f'Cryptography1 initiated in {mode} mode')
    try:
        if key and entry.get():
            try:
                with open(key, 'rb') as f:
                    k = Fernet(f.read())  # Imports the key
                logger.info('Loaded Key')
            except FileNotFoundError:
                raise KeyNotFoundError
            
            encoded = entry.get().encode()  # Encodes the message
            logger.info('Encoded Message')

            if mode == 'Encrypt':
                message = k.encrypt(encoded)  # Encrypts the message
                logger.info(f'Encrypted a message')
            elif mode == 'Decrypt':
                message = k.decrypt(encoded) # Decrypts the message
                logger.info(f'Decrypted a message')
                
            # deletes entry
            entry.delete(0, 'end')

            # Writes the message
            out.config(state='normal')
            out.delete(0, 'end')
            out.insert(0, message)

        elif entry.get() == '':
            logger.info("Finished Cryptography1 because User didn't enter a message")
            messagebox.showwarning(lang.Messages['NoTextTitle'].split('$')[0] + lang.Dialog[mode] + lang.Messages['NoTextTitle'].split('$')[1],lang.Messages['NoTextMessage'] + lang.Dialog[mode])
        elif key == '':
            logger.info("Finished Cryptography1 because User didn't enter a Key")
            messagebox.showwarning(lang.Messages['NoKeyTitle'].split('$')[0] + lang.Dialog[mode] + lang.Messages['NoKeyTitle'].split('$')[1], lang.Messages['NoKeyMessage'].split('$')[0] + lang.Dialog['Key'] + lang.Messages['NoKeyMessage'].split('$')[1] + lang.Dialog[mode])
    except InvalidToken:
        messagebox.showerror(title=lang.Messages['WrongKeyTitle'].split('$')[0] + lang.Dialog['Key'] + lang.Messages['WrongKeyTitle'].split('$')[1], message=lang.Messages['WrongKeyMessage'].split('$')[0] + lang.Dialog['Key'] + lang.Messages['WrongKeyMessage'].split('$')[1])
        logger.exception(f'Decryption failed because of a Decryption Error in {mode} mode')
    except KeyNotFoundError:
        messagebox.showwarning(title=lang.Messages['KeyNotExistTitle'], message=lang.Messages['KeyNotExistMessage'].split('$')[0] + lang.Dialog['Key'] + lang.Messages['KeyNotExistMessage'].split('$')[1])
        logger.info(f"The Key the User tried to Use does Not Exist")
    except Exception:
        messagebox.showerror(title=lang.Messages['UnknownTitle'], message=lang.Messages['UnknownMessage'])
        logger.exception(f'Unknown error/uncaught exception in Cryptography1 - {mode} mode')
    finally:
        out.config(state='readonly')
        logger.info('Cryptography1 finished')

def Cryptography2(mode: str, entry: Entry, out: Entry):
    logger.info(f'Cryptography2 initiated in {mode} mode')
    try:
        filePath = entry.get()
        if key != '' and filePath != '':
            try:
                if os.path.getsize(filePath) >= 1073741824:
                    logger.info(f'shows askYesNoPrompt1 in Cryptography2 {mode} mode')
                    userConfirm = messagebox.askyesno(title=lang.Messages['TooBigTitle'], message=lang.Messages['TooBigMessage2'].split('$')[0] + lang.Dialog[mode] + lang.Messages['TooBigMessage2'].split('$')[1])
                elif os.path.getsize(filePath) >= 100000000:
                    logger.info(f'shows askYesNoPrompt2 in Cryptography2 {mode} mode')
                    userConfirm = messagebox.askyesno(title=lang.Messages['TooBigTitle'], message=lang.Messages['TooBigMessage1'].split('$')[0] + lang.Dialog[mode] + lang.Messages['TooBigMessage1'].split('$')[1])
                else:
                    userConfirm = True
            except FileNotFoundError:
                raise fileNotFoundError
            if userConfirm:
                try:
                    # import Key
                    with open(key, 'rb') as f:
                        k = Fernet(f.read())  # Imports the Key
                    logger.info(f'Loaded Key')
                except FileNotFoundError:
                    raise KeyNotFoundError

                # Load fileContents of file to encrypt
                with open(filePath, 'rb') as f:
                    contents = f.read()
                logger.info(f'Loaded File Contents')

                if mode == 'Encrypt':
                    
                    extension = Path(filePath).suffix
                    output = filedialog.asksaveasfilename(initialdir=os.path.expandvars(filePath[0:filePath.rfind('/') + 1]), defaultextension='.*', initialfile=f'Encrypted {filePath[filePath.rfind("/") + 1:len(filePath.replace(extension, ""))]}', title=lang.Dialog['Save'] + lang.Dialog['Encrypted'] + lang.Dialog['file'], filetypes=(fileTypes[5], fileTypes[0], fileTypes[4]))
                    logger.info('got new filePath')
                    contents = base64.b64encode(extension.encode()) + b'$' + base64.b64encode(k.encrypt(contents)) # Format: extension$contents
                    # writes encrypted Contents to file
                    with open(output, 'wb') as f:
                        f.write(contents)
                    logger.info('Created contents and saved them to filePath')
                else:
                    contents = contents.split(b'$')
                    logger.info('Splitted file into List')

                    contents[1] = k.decrypt(contents[1]).decode()
                    logger.info('Decrypted Contents')

                    output = filedialog.asksaveasfilename(initialdir=os.path.expandvars(filePath[0:filePath.rfind('/') + 1]), defaultextension='.*', initialfile=filePath[filePath.rfind("/") + 1:len(filePath.replace(Path(filePath).suffix, ''))], title=lang.Dialog['Save'] + lang.Dialog['Decrypted'] + lang.Dialog['file'], filetypes=((lang.Dialog['Decrypted'] + lang.Dialog['file'], f'*{base64.b64decode(contents[0]).decode()}' ), fileTypes[4]))
                    logger.info('Got New filePath')
                    with open(output, 'w') as f:
                            f.write(contents[1])
                    logger.info('Saved Contents to filePath')

                # writes filePath2 to out
                out.config(state='normal')
                out.delete(0, 'end')
                out.insert(0, output)
                logger.info('Inserted output into out')
        elif filePath == '':
            logger.info("Finished Cryptography2 because User didn't enter a message")
            messagebox.showwarning(lang.Messages['NoTextTitle'].split('$')[0] + lang.Dialog[mode] + lang.Messages['NoTextTitle'].split('$')[1],lang.Messages['NoTextMessage'] + lang.Dialog[mode])
        elif key == '':
            logger.info("Finished Cryptography2 because User didn't enter a Key")
            messagebox.showwarning(lang.Messages['NoKeyTitle'].split('$')[0] + lang.Dialog['Key'] + lang.Messages['NoKeyTitle'].split('$')[1], lang.Messages['NoKeyMessage'].split('$')[0] + lang.Dialog['Key'] + lang.Messages['NoKeyMessage'].split('$')[1] + lang.Dialog[mode])
    except ValueError:
        messagebox.showerror(title=lang.Dialog[f'{mode}ion'] + lang.Messages['ValueTitle'], message=lang.Dialog[f'{mode}ion'] + lang.Messages['ValueMessage'])
        logger.exception(f"Showed ValueError")
    except fileNotFoundError:
        messagebox.showwarning(title=lang.Messages['fileNotFoundTitle'], message=lang.Messages['fileNotFoundMessage'])
        logger.info(f"The File The User Tried To Use didn't Exist")
    except InvalidToken:
        messagebox.showerror(title=f'Wrong Key entered!', message=f'This is the wrong Key to {mode} this message! Use the right Key!')
        logger.exception(f'Decryption failed because of a Decryption Error in {mode} mode')
    except MemoryError:
        messagebox.showerror(title=lang.Dialog[f'{mode}ion'] + lang.Messages['TooBigTitle'], message=lang.Messages['TooBigMessage'].split('$')[0] + lang.Dialog[f'{mode}ed'] + lang.Messages['TooBigMessage'].split('$')[1])
        logger.info(f'{mode}ion failed, file was too big')
    except KeyNotFoundError:
        messagebox.showwarning(title=lang.Messages['KeyNotExistTitle'], message=lang.Messages['KeyNotExistMessage'].split('$')[0] + lang.Dialog['Key'] + lang.Messages['KeyNotExistMessage'].split('$')[1])
        logger.info(f"The Key the User tried to Use does Not Exist")
    except FileNotFoundError:
        pass
    except Exception:
        messagebox.showerror(title=lang.Messages['UnknownTitle'], message=lang.Messages['UnknownMessage'])
        logger.exception(f'Unknown error/uncaught exception in Cryptography2 - {mode} mode')
    finally:
        out.config(state='readonly')
        logger.info('Cryptography2 finished')



def Window(EncryptFrame: Frame, DecryptFrame: Frame, KeyFrame, out: Entry, l: str):
    global fileTypes, img, lang, key, IndicatorTooltip, Indicator
    from Cryptographer import LoadLang, LoadFileTypes

    # Lang Configuration
    lang = LoadLang(l)
    fileTypes = LoadFileTypes(lang)
    
    # Key Input
    key = ''
    Button(KeyFrame, text=lang.Main['BrowseKeyBtn'], command=lambda: BrowseKeyDialog(KeyFrame)).grid(row=0, column=0, pady=2)
    Button(KeyFrame, text=lang.Main['GenerateKeyBtn'], command=GenerateKey).grid(row=1, column=0, padx=10, pady=6)
    if key == '':
        img = ImageTk.PhotoImage(Image.open('UI/NotLoaded.ico').resize((40, 40)))
    else:
        img = ImageTk.PhotoImage(Image.open('UI/Loaded.ico').resize((40, 40)))
    Indicator = Label(KeyFrame, image=img) # LoadIndicator
    Indicator.grid(row=0, column=1, rowspan=2, padx=5)
    IndicatorTooltip = ToolTip(Indicator, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['NotLoaded'], delay=1.0) # Tooltip for LoadIndicator
    logger.info('Loaded Key options')


    # Encrypt option 1
    Label(EncryptFrame, text=lang.Main['Encrypt1Title']).grid(row=0, column=0) # Description Label
    Encrypt1Entry = Entry(EncryptFrame, width=40) # Define Entry
    Encrypt1Entry.grid(row=1, column=0, padx=5) # Put Entry on screen
    Button(EncryptFrame, text=lang.Main['Encrypt'], command=lambda: Cryptography1('Encrypt', Encrypt1Entry, out)).grid(row=1, column=1) # Encrypt Btn

    # Encrypt option 2
    Label(EncryptFrame, text=lang.Main['Encrypt2Title']).grid(row=2, column=0) # Description Label
    Encrypt2Entry = Entry(EncryptFrame, width=40) # Define Entry
    Encrypt2Entry.grid(row=3, column=0, padx=5, pady=5) # Put Entry on screen
    Button(EncryptFrame, text=lang.Main['Encrypt'], command=lambda: Cryptography2('Encrypt', Encrypt2Entry, out)).grid(row=3,column=1) # Encrypt Btn
    Button(EncryptFrame, text=lang.Main['BrowseBtn'], command=lambda: BrowseEncryptDialog(Encrypt2Entry)).grid(row=3, column=2, padx=(0,5)) # BrowseCryptographyDialog
    logger.info('loaded encrypt options')


    # Decrypt option 1
    Label(DecryptFrame, text=lang.Main['Decrypt1Title']).grid(row=0, column=0) # Description Label
    Decrypt1Entry = Entry(DecryptFrame, width=40) # Define Entry
    Decrypt1Entry.grid(row=1, column=0, padx=5) # Put Entry on screen
    Button(DecryptFrame, text=lang.Main['Decrypt'], command=lambda: Cryptography1('Decrypt', Decrypt1Entry, out)).grid(row=1, column=1) # Decrypt Btn

    # Decrypt option 2
    Label(DecryptFrame, text=lang.Main['Decrypt2Title']).grid(row=2, column=0) # Description Label
    Decrypt2Entry = Entry(DecryptFrame, width=40) # Define Entry
    Decrypt2Entry.grid(row=3, column=0, padx=5, pady=5) # Put Entry on screen
    Button(DecryptFrame, text=lang.Main['Decrypt'], command=lambda: Cryptography2('Decrypt', Decrypt2Entry, out)).grid(row=3,column=1) # Decrypt Btn
    Button(DecryptFrame, text=lang.Main['BrowseBtn'], command=lambda: BrowseDecryptDialog(Decrypt2Entry)).grid(row=3, column=2, padx=(0,5)) # BrowseDecryptDialog
    logger.info('loaded decrypt options')
>>>>>>> dev
