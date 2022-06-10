import base64
from tkinter import UNDERLINE, filedialog, messagebox, Tk, Label, Button, Entry, LabelFrame, font
from cryptography.fernet import Fernet, InvalidToken
import pathlib
import logging
import os

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


class fileNotFoundError(FileNotFoundError):
    pass
class KeyNotFoundError(FileNotFoundError):
    pass


def BrowseKeyDialog(keyEntry: Entry):
    browseKeyDialog = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=lang.Dialog['Open'] + lang.Dialog['Key'], filetypes=(fileTypes[6], fileTypes[4]))
    if browseKeyDialog:
        logger.info(f'User selected Key')
        keyEntry.delete(0,"end")
        keyEntry.insert(0, browseKeyDialog)

def BrowseEncryptDialog(encrypt2Entry: Entry):
    browseEncryptDialog = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=lang.Dialog['Open'] + lang.Dialog['file'] + lang.Dialog['Encrypt'], filetypes=(fileTypes[0], fileTypes[1], fileTypes[2], fileTypes[3], fileTypes[4]))
    if browseEncryptDialog:
        logger.info('User selected file to Encrypt')
        encrypt2Entry.delete(0,"end")
        encrypt2Entry.insert(0, browseEncryptDialog)

def BrowseDecryptDialog(decrypt2Entry: Entry):
    browseDecryptDialog = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=lang.Dialog['Open'] + lang.Dialog['file'] + lang.Dialog['Decrypt'], filetypes=(fileTypes[5], fileTypes[0]))
    if browseDecryptDialog:
        logger.info('User selected file to Decrypt')
        decrypt2Entry.delete(0,"end")
        decrypt2Entry.insert(0, browseDecryptDialog)

def GenerateKey(keyEntry: Entry):
    keyPath = filedialog.asksaveasfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), defaultextension='.*', initialfile=lang.Dialog['Key'], title=lang.Dialog['Save'] + lang.Dialog['Key'], filetypes=(fileTypes[6], fileTypes[4]))

    if keyPath:
        logger.info('User generated key')
        keyEntry.delete(0,"end")
        keyEntry.insert(0, keyPath)
        with open(keyPath, 'wb') as f:
            f.write(Fernet.generate_key())

def Cryptography1(mode: str, entry: Entry, keyEntry: Entry):
    logger.info(f'Cryptography1 initiated in {mode} mode')
    keyPath = keyEntry.get()
    try:
        if keyPath and entry.get():
            try:
                with open(keyPath, 'rb') as f:
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
            messagebox.showwarning(f'No Text to {mode} entered', f'You Need to Enter a Message Before You Try to {mode}')
        elif keyEntry.get() == '':
            logger.info("Finished Cryptography1 because User didn't enter a Key")
            messagebox.showwarning(f'No text to {mode} entered', f'You Need to Insert a Key Before You Try to {mode}')
    except KeyNotFoundError:
        messagebox.showwarning(title=f'Key not found', message=f"The Key You tried to Use Does Not Exist!\nPlease use an Existing Key!")
        logger.info(f"The Key the User tried to Use does Not Exist")
    except MemoryError:
        messagebox.showerror(title=f'{mode}ion failed', message=f"The message couldn't be {mode}ed because it was too big!")
        logger.info(f'{mode}ion failed, file was too big')
    except InvalidToken:
        messagebox.showerror(title=f'Wrong Key entered!', message=f'This is the wrong Key to {mode} this message! Use the right Key!')
        logger.exception(f'Decryption failed because of a Decryption Error in {mode} mode')
    except Exception:
        messagebox.showerror(title='Unknown Error', message=f'An Unknown Error occurred.\nPlease open an issue at https://github.com/jasger9000/Cryptographer and attach the log file of your current session.\nLog file: {os.getcwd()}/Cryptographer.log')
        logger.exception(f'Unknown error/uncaught exception in Cryptography1 - {mode} mode')
    finally:
        out.config(state='readonly')
        logger.info('Cryptography1 finished')

def Cryptography2(mode: str, entry: Entry, keyEntry: Entry):
    logger.info(f'Cryptography2 initiated in {mode} mode')
    try:
        keyPath = keyEntry.get()
        filePath = entry.get()
        if keyPath and filePath:
            try:
                # Checks for user conformation if file is too big
                if os.path.getsize(filePath) >= 1073741824:
                    logger.info(f'shows askYesNoPrompt1 in Cryptography2 {mode} mode')
                    userConfirm = messagebox.askyesno(title='file too big', message=f'File larger than 1 Gigabyte will take several minutes to {mode} or will fail,\nwould you still like to proceed?')
                elif os.path.getsize(filePath) >= 100000000:
                    logger.info(f'shows askYesNoPrompt2 in Cryptography2 {mode} mode')
                    userConfirm = messagebox.askyesno(title='file too big', message=f'File larger than 100mb could take a long time to {mode},\nwould you still like to proceed?')
                else:
                    userConfirm = True
            except FileNotFoundError:
                raise fileNotFoundError
            if userConfirm:
                try:
                    # import Key
                    with open(keyPath, 'rb') as f:
                        k = Fernet(f.read())  # Imports the Key
                    logger.info(f'Loaded Key')
                except FileNotFoundError:
                    raise KeyNotFoundError

                # Load fileContents of file to encrypt
                with open(filePath, 'rb') as f:
                    contents = f.read()
                logger.info(f'Loaded File Contents')

                if mode == 'Encrypt':
                    extention = pathlib.Path(filePath).suffix
                    output = filedialog.asksaveasfilename(initialdir=os.path.expandvars(filePath[0:filePath.rfind('/') + 1]), defaultextension='.*', initialfile=f'Encrypted {filePath[filePath.rfind("/") + 1:len(filePath.replace(extention, ""))]}', title='Save Encrypted file...', filetypes=(('Encrypted file', '*.Encrypted'),('Text file', '*.txt'),('Any file', '*.*')))
                    logger.info('got new filePath')
                    contents = base64.b64encode(extention.encode()) + b'$' + base64.b64encode(k.encrypt(contents)) # Format: extension$contents
                    # writes encrypted Contents to file
                    with open(output, 'wb') as f:
                        f.write(contents)
                    logger.info('Created contents and saved them to filePath')
                else:
                    contents = contents.split(b'$')
                    logger.info('Splitted file into List')

                    contents[1] = k.decrypt(contents[1]).decode()
                    logger.info('Decrypted Contents')

                    output = filedialog.asksaveasfilename(initialdir=os.path.expandvars(filePath[0:filePath.rfind('/') + 1]), defaultextension='.*', initialfile=filePath[filePath.rfind("/") + 1:len(filePath.replace(pathlib.Path(filePath).suffix, ''))], title='Save Decrypted file...', filetypes=(('Decrypted file',f'*{base64.b64decode(contents[0]).decode()}' ),('Any file', '*.*')))
                    logger.info('Got New filePath')
                    with open(output, 'w') as f:
                            f.write(contents[1])
                    logger.info('Saved Contents to filePath')

                # writes filePath2 to out
                out.config(state='normal')
                out.delete(0, 'end')
                out.insert(0, output)
                logger.info('Inserted output into out')
        elif len(keyPath) == 0:
            logger.info("Finished Cryptography2 because User didn't enter a Key")
            messagebox.showwarning(f'No text to {mode} entered', f'You Need to Insert a Key Before You Try to {mode}')
        elif len(filePath) == 0:
            logger.info("Finished Cryptography2 because User didn't enter a filePath")
            messagebox.showwarning(f'No File to {mode} entered', f'You Need to Enter a File Path Before You Try to {mode}')
        return
    except ValueError:
        messagebox.showerror(title=f'{mode}ion failed', message=f"The file couldn't be {mode}ed because the file type is not supported!")
        logger.exception(f"Showed ValueError")
    except InvalidToken:
        messagebox.showerror(title=f'Wrong Key entered!', message=f'This is the wrong Key to {mode} this message! Use the right Key!')
        logger.exception(f'Decryption failed because of a Decryption Error in {mode} mode')
    except MemoryError:
        messagebox.showerror(title=f'{mode}ion failed', message=f"The message couldn't be {mode}ed because it was too big!")
        logger.info(f'{mode}ion failed, file was too big')
    except fileNotFoundError:
        messagebox.showwarning(title='File not found', message=f'The File you would Like to {mode} was not Found!\nPlease Use an Existing File!')
        logger.info(f"The File The User Tried To Use didn't Exist")
    except KeyNotFoundError:
        messagebox.showwarning(title=f'Key not found', message=f"The Key You tried to Use Does Not Exist!\nPlease use an Existing Key!")
        logger.info(f"The Key the User tried to Use does Not Exist")
    except Exception:
        messagebox.showerror(title='Unknown Error', message=f'An Unknown Error occurred.\nPlease open an issue at https://github.com/jasger9000/Cryptographer and attach the log file of your current session.\nLog file: {os.getcwd()}/Cryptographer.log')
        logger.exception(f'Unknown error/uncaught exception in Cryptography2 - {mode} mode')
    finally:
        out.config(state='readonly')
        logger.info('Cryptography2 finished')

def Copy(root: Tk):
    logger.info('Copy function initiated')
    try:
        root.clipboard_clear()
        root.clipboard_append(out.get())
    except Exception:
        logger.exception(f'Unknown error/uncaught exception in Copy function')
        messagebox.showerror(title='Unknown error', message=f'An Unknown Error occurred.\nPlease open an issue at https://github.com/jasger9000/Cryptographer and attach the log file of your current session.\nLog file: {os.getcwd()}/Cryptographer.log')
    finally:
        logger.info('Copy function finished')

def Delete():
    logger.info('Delete function initiated')
    try:
        out.config(state='normal')
        out.delete(0, 'end')
    except Exception:
        logger.exception(f'Unknown/uncaught exception in Delete function')
        messagebox.showerror(title='Unknown Error', message=f'An Unknown Error occurred.\nPlease open an issue at https://github.com/jasger9000/Cryptographer and attach the log file of your current session.\nLog file: {os.getcwd()}/Cryptographer.log')
    finally:
        out.config(state='readonly')
        logger.info('Delete function finished')

def main(root: Tk, version: str):
    global out

    # GUI Configuration
    root.title(f'Symmetric Cryptographer ver. {version}')
    root.geometry('')
    TitleLabel = Label(root, text='Symmetric Cryptographer', font=('Helvetica', 14, font.BOLD, UNDERLINE))
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
    Button(frame1, text='Encrypt', command=lambda: Cryptography1('Encrypt', encrypt1Entry, KeyEntry)).grid(row=1, column=1) # Encrypt Btn

    # Encrypt option 2
    Label(frame1, text='\n\nEncrypt a file:').grid(row=2, column=0) # Description Label
    encrypt2Entry = Entry(frame1, font=('Arial', 14), width=20) # Define Entry
    encrypt2Entry.grid(row=3, column=0) # Put Entry on screen
    Button(frame1, text='Encrypt', command=lambda: Cryptography2('Encrypt', encrypt2Entry, KeyEntry)).grid(row=3,column=1) # Encrypt Btn
    Button(frame1, text='Browse', command=lambda: BrowseEncryptDialog(encrypt2Entry)).grid(row=3, column=2) # BrowseCryptographyDialog
    logger.info('loaded encrypt options')

    # Decryption Frame
    frame2 = LabelFrame(root, text='Decrypt', font=('Arial', 12), padx=10, pady=12)
    frame2.grid(row=2, column=1, padx=10, pady=10)

    # Decrypt option 1
    Label(frame2, text='Decrypt a message:').grid(row=0, column=0) # Description Label
    decrypt1Entry = Entry(frame2, font=('Arial', 14), width=20) # Define Entry
    decrypt1Entry.grid(row=1, column=0) # Put Entry on screen
    Button(frame2, text='Decrypt', command=lambda: Cryptography1('Decrypt', decrypt1Entry, KeyEntry)).grid(row=1, column=1) # Decrypt Btn

    # Decrypt option 2
    Label(frame2, text='\n\nDecrypt a file:').grid(row=2, column=0) # Description Label
    decrypt2Entry = Entry(frame2, font=('Arial', 14), width=20) # Define Entry
    decrypt2Entry.grid(row=3, column=0) # Put Entry on screen
    Button(frame2, text='Decrypt', command=lambda: Cryptography2('Decrypt', decrypt2Entry, KeyEntry)).grid(row=3,column=1) # Decrypt Btn
    Button(frame2, text='Browse', command=lambda: BrowseDecryptDialog(decrypt2Entry)).grid(row=3, column=2) # BrowseDecryptDialog
    logger.info('loaded decrypt options')

    # Output
    frame3 = LabelFrame(root, text='Output:', font=('Arial', 12, UNDERLINE), padx=10, pady=12, borderwidth=0)
    frame3.grid(row=3, column=0, padx=10, columnspan=2)

    Button(frame3, text='Delete', command=Delete).grid(row=0, column=0)
    out = Entry(frame3, font=('Arial', 14), width=27, state='readonly')
    out.grid(row=0, column=1)
    Button(frame3, text='Copy', command=lambda: Copy(root)).grid(row=0, column=2)


    return frame0, frame1, frame2, frame3, TitleLabel


def Unload(frame0: LabelFrame,frame1: LabelFrame,frame2: LabelFrame,frame3: LabelFrame, TitleLabel: Label):
    frame0.destroy()
    frame1.destroy()
    frame2.destroy()
    frame3.destroy()
    TitleLabel.destroy()
