from tkinter import UNDERLINE, filedialog, messagebox, Tk, Label, Button, Entry, LabelFrame
from tkinter.font import BOLD
from cryptography.fernet import Fernet, InvalidToken
from pathlib import Path
import logging
from os.path import expandvars, getsize
from os import getcwd

# TODO Make User send log to me

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
    if browseEncryptDialog:
        logger.info('User selected file to Encrypt')
        encrypt2Entry.delete(0,"end")
        encrypt2Entry.insert(0, browseEncryptDialog)
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
    root.title(f'Symmetric Cryptographer {version}')
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
