from tkinter import UNDERLINE, filedialog, messagebox
from tktooltip import ToolTip 
from PIL import ImageTk, Image
from tkinter.ttk import Button, Frame, Label, Entry, LabelFrame
from cryptography.fernet import Fernet
import rsa
import base64
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
class PrivKeyNotFoundError(FileNotFoundError):
    pass
class PubKeyNotFoundError(FileNotFoundError):
    pass

def BrowseKeyDialog(mode: str, KeyFrame: Frame):
    global IndicatorTooltip1, IndicatorTooltip2, pubKey, privKey

    if mode == 'Private':
        type = 7
    else:
        type = 8
    
    key = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=lang.Dialog['Open'] + lang.Dialog[mode], filetypes=(fileTypes[type], fileTypes[4]))
    
    if mode == 'Public':
        pubKey = key
        if key:
            if int(config['Settings']['savelastkey']) == 1:
                config.set('State', 'publickeyfile', key)
                with open('config.ini', 'w') as f:
                    config.write(f)
            Indicator1.config(image=img1)
            IndicatorTooltip1 = ToolTip(Indicator1, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['Loaded'], delay=1.0) # Tooltip for LoadIndicator
    else:
        privKey = key
        if key:
            if int(config['Settings']['savelastkey']) == 1:
                config.set('State', 'privatekeyfile', key)
                with open('config.ini', 'w') as f:
                    config.write(f)
            Indicator2.config(image=img1)
            IndicatorTooltip2 = ToolTip(Indicator2, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['Loaded'], delay=1.0) # Tooltip for LoadIndicator


def BrowseEncryptDialog(encrypt2Entry: Entry):
    browseEncryptDialog = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=lang.Dialog['Open'] + lang.Dialog['file'] + lang.Dialog['to'] + lang.Dialog['Encrypt'], filetypes=(fileTypes[0], fileTypes[1], fileTypes[2], fileTypes[3], fileTypes[4]))
    if browseEncryptDialog:
        logger.info('User selected file to Encrypt')
        encrypt2Entry.delete(0,"end")
        encrypt2Entry.insert(0, browseEncryptDialog)

def BrowseDecryptDialog(decrypt2Entry: Entry):
    browseDecryptDialog = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=lang.Dialog['Open'] + lang.Dialog['file'] + lang.Dialog['to'] + lang.Dialog['Decrypt'], filetypes=(fileTypes[5], fileTypes[0]))
    if browseDecryptDialog:
        logger.info('User selected file to Decrypt')
        decrypt2Entry.delete(0,"end")
        decrypt2Entry.insert(0, browseDecryptDialog) 

def GenerateKeyPair(KeyFrame: Frame):
    global IndicatorTooltip1, IndicatorTooltip2, pubKey, privKey

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
            
            if int(config['Settings']['savelastkey']) == 1:
                config.set('State', 'publickeyfile', pubKey)
                with open('config.ini', 'w') as f:
                    config.write(f)
            Indicator1.config(image=img1)
            IndicatorTooltip1 = ToolTip(Indicator1, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['Loaded'], delay=1.0) # Tooltip for LoadIndicator
            
            if int(config['Settings']['savelastkey']) == 1:
                config.set('State', 'privatekeyfile', privKey)
                with open('config.ini', 'w') as f:
                    config.write(f)
            Indicator2.config(image=img1)
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
                    with open(pubKey, 'rb') as f:
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
        logger.exception(f'Unknown error/uncaught exception in Cryptography1 - {mode} mode')
    finally:
        out.config(state='readonly')
        logger.info('Cryptography1 finished')

        
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
                else:
                    userConfirm = True
            except FileNotFoundError:
                raise fileNotFoundError
            if userConfirm:
                try:
                    with open(privKey, 'rb') as f:
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
                    extension = os.path(filePath)
                    output = filedialog.asksaveasfilename(initialdir=os.path.expandvars(filePath[0:filePath.rfind('/') + 1]), defaultextension='.*', initialfile=f'Encrypted {filePath[filePath.rfind("/") + 1:len(filePath.replace(extension, ""))]}', title=lang.Dialog['Save'] + lang.Dialog['Encrypted'] + lang.Dialog['file'], filetypes=(fileTypes[5],fileTypes[0],fileTypes[4]))
                    logger.info('got new filePath')
                    try:
                        with open(pubKey, 'rb') as f:
                            publicKey = f.read()
                        logger.info('Loaded Public Key')
                    except FileNotFoundError:
                        raise PubKeyNotFoundError
                    
                    contents = Fernet(symKey).encrypt(contents)
                    symKey = rsa.encrypt(symKey, rsa.PublicKey.load_pkcs1(publicKey))
                    contents = base64.b64encode(extension.encode()) + b'$' + base64.b64encode(symKey) + b'$' + base64.b64encode(contents) # Format: extension$symKey$contents
                    with open(output, 'wb') as f:
                        f.write(contents)
                    logger.info('Created contents and saved them to filePath')
                else:
                    contents = contents.split(b'$')
                    logger.info('Splitted file into List')
                    symKey = Fernet(rsa.decrypt(base64.b64decode(contents[1]), rsa.PrivateKey.load_pkcs1(privateKey)))
                    contents[2] = symKey.decrypt(base64.b64decode(contents[2])).decode()
                    logger.info('Decrypted Contents')

                    output = filedialog.asksaveasfilename(initialdir=os.path.expandvars(filePath[0:filePath.rfind('/') + 1]), defaultextension='.*', initialfile=filePath[filePath.rfind("/") + 1:len(filePath.replace(os.path(filePath), ''))], title=lang.Dialog['Save'] + lang.Dialog['Decrypted'] + lang.Dialog['file'], filetypes=((lang.Dialog['Decrypted'] + lang.Dialog['file'],f'*{base64.b64decode(contents[0]).decode()}' ),fileTypes[4]))
                    logger.info('Got New filePath')
                    with open(output, 'w') as f:
                        f.write(contents[2])
                    logger.info('Saved Contents to filePath')

                out.config(state='normal')
                out.delete(0, 'end')
                out.insert(0, output)
                logger.info('Inserted output into out')
        elif entry.get() == '':
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
        logger.exception(f'Unknown error/uncaught exception in Cryptography2 - {mode} mode')
    finally:
        out.config(state='readonly')
        logger.info('Cryptography2 finished')
    

def Window(EncryptFrame: Frame, DecryptFrame: Frame, KeyFrame: LabelFrame, out: Entry, l: str):
    global fileTypes, lang, privKey, pubKey, Indicator1, IndicatorTooltip1, img1, Indicator2, IndicatorTooltip2, img2, config
    from Cryptographer import LoadFileTypes, LoadConfig, resource_path
    
    # Lang Configuration
    config, lang = LoadConfig()
    fileTypes = LoadFileTypes(lang)
    
    img1 = ImageTk.PhotoImage(Image.open(resource_path('UI/Loaded.ico')).resize((40, 40)))
    img2 = ImageTk.PhotoImage(Image.open(resource_path('UI/NotLoaded.ico')).resize((40, 40)))

    # Public Key Input
    if config['State']['publickeyfile'] != 'None':
        pubKey = config['State']['publickeyfile']
        Indicator1 = Label(KeyFrame, image=img1) # LoadIndicator
        IndicatorTooltip1 = ToolTip(Indicator1, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['Loaded'], delay=1.0) # Tooltip for LoadIndicator
    else:
        pubKey = ''
        Indicator1 = Label(KeyFrame, image=img2) # LoadIndicator
        IndicatorTooltip1 = ToolTip(Indicator1, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['NotLoaded'], delay=1.0) # Tooltip for LoadIndicator
    Indicator1.grid(row=1, column=1, padx=5)
    Label(KeyFrame, text=lang.AsymMain['PublicKeyTitle'], font=('Arial', 12, UNDERLINE)).grid(row=0, column=0, columnspan=2)
    Button(KeyFrame, text=lang.Main['BrowseBtn'], command=lambda: BrowseKeyDialog('Public', KeyFrame)).grid(row=1, column=0)
    logger.info('loaded PublicKey input') # Section Loaded
    
    Button(KeyFrame, text=lang.AsymMain['GenerateKeyBtn'], command=lambda: GenerateKeyPair(KeyFrame)).grid(row=2, column=0, pady=5, padx=(5,0))

    # Private Key Input
    if config['State']['privatekeyfile'] != 'None':
        privKey = config['State']['privatekeyfile']
        Indicator2 = Label(KeyFrame, image=img1) # LoadIndicator
        IndicatorTooltip2 = ToolTip(Indicator2, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['Loaded'], delay=1.0) # Tooltip for LoadIndicator
    else:
        privKey = ''
        Indicator2 = Label(KeyFrame, image=img2) # LoadIndicator
        IndicatorTooltip2 = ToolTip(Indicator2, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['NotLoaded'], delay=1.0) # Tooltip for LoadIndicator
    Label(KeyFrame, text=lang.AsymMain['PrivateKeyTitle'],font=('Arial', 12, UNDERLINE)).grid(row=3, column=0, columnspan=2)
    Button(KeyFrame, text=lang.Main['BrowseBtn'], command=lambda: BrowseKeyDialog('Private', KeyFrame)).grid(row=4, column=0)
    Indicator2.grid(row=4, column=1, padx=5, pady=5)
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
    Button(EncryptFrame, text=lang.Main['BrowseBtn'], command=lambda: BrowseEncryptDialog(Encrypt2Entry)).grid(row=3, column=2, padx=(0,5), pady=5) 
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