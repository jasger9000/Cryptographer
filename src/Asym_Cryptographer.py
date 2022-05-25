from tkinter import UNDERLINE, filedialog, messagebox, Tk, Label, Button, Entry, LabelFrame, font
from cryptography.fernet import Fernet
import rsa
import base64
import logging
import pathlib
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


class fileNotFoundError(FileNotFoundError):
    pass
class PrivKeyNotFoundError(FileNotFoundError):
    pass
class PubKeyNotFoundError(FileNotFoundError):
    pass

def BrowseKeyDialog(keyEntry: Entry, mode: str):
    if mode == 'Private':
        type = 'priv_key'
    else:
        type = 'pub_key'
    browseKeyDialog = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=f'Open {mode} Key...', filetypes=((f'{mode} Key files', f'*.{type}'), fileTypes[4]))
    if browseKeyDialog:
        logger.info(f'User selected {mode} ')
        keyEntry.delete(0,"end")
        keyEntry.insert(0, browseKeyDialog)

def BrowseEncryptDialog(encrypt2Entry: Entry):
    browseEncryptDialog = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=f'Select file to Encrypt...', filetypes=(fileTypes[0], fileTypes[1], fileTypes[2], fileTypes[3], fileTypes[4]))
    if browseEncryptDialog:
        logger.info('User selected file to Encrypt')
        encrypt2Entry.delete(0,"end")
        encrypt2Entry.insert(0, browseEncryptDialog)

def BrowseDecryptDialog(decrypt2Entry: Entry):
    browseDecryptDialog = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=f'Select file to Decrypt...', filetypes=(fileTypes[5], fileTypes[0]))
    if browseDecryptDialog:
        logger.info('User selected file to Decrypt')
        decrypt2Entry.delete(0,"end")
        decrypt2Entry.insert(0, browseDecryptDialog) 

def GenerateKeyPair(keyEntry: Entry):
    logger.info('Initiated GenerateKeyPair')
    publickeyPath = filedialog.asksaveasfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), defaultextension='.*', initialfile=os.path.expandvars("$USERNAME's Public Key"), title='Save new Key...', filetypes=(fileTypes[7], fileTypes[4]))
    if publickeyPath:
        privateKeyPath = filedialog.asksaveasfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), defaultextension='.*', initialfile="Private Key", title='Save new Key...', filetypes=(fileTypes[6], fileTypes[4]))
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
                    with open(PublicKeyEntry.get(), 'rb') as f:
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
        messagebox.showerror(title='Unknown Error', message=f'An Unknown Error occurred.\nPlease open an issue at https://github.com/jasger9000/Cryptographer and attach the log file of your current session.\nLog file: {os.getcwd()}/Cryptographer.log')
        logger.exception(f'Unknown error/uncaught exception in Cryptography1 - {mode} mode')
    finally:
        out.config(state='readonly')
        logger.info('Cryptography1 finished')

        
def Cryptography2(mode: str, entry: Entry, PublicKeyEntry: Entry, PrivateKeyEntry: Entry, out: Entry):
    logger.info(f'Cryptography2 initiated in {mode} mode')
    try:
        if entry.get() and PublicKeyEntry.get() and PrivateKeyEntry.get():
            filePath = entry.get()
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
                    with open(PrivateKeyEntry.get(), 'rb') as f:
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
                    extention = pathlib.Path(filePath).suffix
                    output = filedialog.asksaveasfilename(initialdir=os.path.expandvars(filePath[0:filePath.rfind('/') + 1]), defaultextension='.*', initialfile=f'Encrypted {filePath[filePath.rfind("/") + 1:len(filePath.replace(extention, ""))]}', title='Save Encrypted file...', filetypes=(('Encrypted file', '*.Encrypted'),('Text file', '*.txt'),('Any file', '*.*')))
                    logger.info('got new filePath')
                    try:
                        with open(PublicKeyEntry.get(), 'rb') as f:
                            publicKey = f.read()
                        logger.info('Loaded Public Key')
                    except FileNotFoundError:
                        raise PubKeyNotFoundError
                    
                    contents = Fernet(symKey).encrypt(contents)
                    symKey = rsa.encrypt(symKey, rsa.PublicKey.load_pkcs1(publicKey))
                    contents = base64.b64encode(extention.encode()) + b'$' + base64.b64encode(symKey) + b'$' + base64.b64encode(contents) # Format: extention$symKey$contents
                    with open(output, 'wb') as f:
                        f.write(contents)
                    logger.info('Created contents and saved them to filePath')
                else:
                    contents = contents.split(b'$')
                    logger.info('Splitted file into List')
                    symKey = Fernet(rsa.decrypt(base64.b64decode(contents[1]), rsa.PrivateKey.load_pkcs1(privateKey)))
                    contents[2] = symKey.decrypt(base64.b64decode(contents[2])).decode()
                    logger.info('Decrypted Contents')

                    output = filedialog.asksaveasfilename(initialdir=os.path.expandvars(filePath[0:filePath.rfind('/') + 1]), defaultextension='.*', initialfile=filePath[filePath.rfind("/") + 1:len(filePath.replace(pathlib.Path(filePath).suffix, ''))], title='Save Decrypted file...', filetypes=(('Decrypted file',f'*{base64.b64decode(contents[0]).decode()}' ),('Any file', '*.*')))
                    logger.info('Got New filePath')
                    with open(output, 'w') as f:
                        f.write(contents[2])
                    logger.info('Saved Contents to filePath')

                out.config(state='normal')
                out.delete(0, 'end')
                out.insert(0, output)
                logger.info('Inserted output into out')
        elif entry.get() == '':
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
        messagebox.showerror(title='Unknown Error', message=f'An Unknown Error occurred.\nPlease open an issue at https://github.com/jasger9000/Cryptographer and attach the log file of your current session.\nLog file: {os.getcwd()}/Cryptographer.log')
        logger.exception(f'Unknown error/uncaught exception in Cryptography2 - {mode} mode')
    finally:
        out.config(state='readonly')
        logger.info('Cryptography2 finished')
    
def Copy(root: Tk, out: Entry):
    logger.info('Copy function initiated')
    try:
        root.clipboard_clear()
        root.clipboard_append(out.get())
    except Exception:
        logger.exception(f'Unknown error/uncaught exception in Copy function')
        messagebox.showerror(title='Unknown error', message=f'An Unknown Error occurred.\nPlease open an issue at https://github.com/jasger9000/Cryptographer and attach the log file of your current session.\nLog file: {os.getcwd()}/Cryptographer.log')
    finally:
        logger.info('Copy function finished')

def Delete(out: Entry):
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
    # GUI Configuration
    root.title(f'Asymmetric Cryptographer ver. {version}')
    root.geometry('')
    TitleLabel = Label(root, text='Asymmetric Cryptographer', font=('Helvetica', 14, font.BOLD, UNDERLINE))
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

