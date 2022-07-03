import base64
from tkinter import filedialog, messagebox
from tktooltip import ToolTip 
from PIL import ImageTk, Image
from tkinter.ttk import Button, Entry, Frame, Label
from cryptography.fernet import Fernet, InvalidToken
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


def BrowseKeyDialog(KeyFrame):
    global key, IndicatorTooltip
    key = filedialog.askopenfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), title=lang.Dialog['Open'] + lang.Dialog['Key'], filetypes=(fileTypes[6], fileTypes[4]))
    if key:
        if int(config['Settings']['savelastkey']) == 1:
            config.set('State', 'keyfile', key)
            with open('config.ini', 'w') as f:
                config.write(f)
        Indicator.config(image=img1)
        IndicatorTooltip = ToolTip(Indicator, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['Loaded'], delay=1.0) # Tooltip for LoadIndicator
        

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

def GenerateKey():
    global key, IndicatorTooltip

    key = filedialog.asksaveasfilename(initialdir=os.path.expandvars(R'C:\Users\$USERNAME\Documents'), defaultextension='.*', initialfile=lang.Dialog['Key'], title=lang.Dialog['Save'] + lang.Dialog['Key'], filetypes=(fileTypes[6], fileTypes[4]))
    if key:
        logger.info('User generated key')
        with open(key, 'wb') as f:
            f.write(Fernet.generate_key())
        if int(config['Settings']['savelastkey']) == 1:
            config.set('State', 'keyfile', key)
            with open('config.ini', 'w') as f:
                config.write(f)
        Indicator.config(image=img1)
        IndicatorTooltip = ToolTip(Indicator, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['Loaded'], delay=1.0) # Tooltip for LoadIndicator
        

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
                    
                    extension = os.path.splitext(filePath)
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

                    output = filedialog.asksaveasfilename(initialdir=os.path.expandvars(filePath[0:filePath.rfind('/') + 1]), defaultextension='.*', initialfile=filePath[filePath.rfind("/") + 1:len(filePath.replace(os.path.splitext(filePath), ''))], title=lang.Dialog['Save'] + lang.Dialog['Decrypted'] + lang.Dialog['file'], filetypes=((lang.Dialog['Decrypted'] + lang.Dialog['file'], f'*{base64.b64decode(contents[0]).decode()}' ), fileTypes[4]))
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


def Window(EncryptFrame: Frame, DecryptFrame: Frame, KeyFrame, out: Entry):
    global fileTypes, img1, img2, lang, key, IndicatorTooltip, Indicator, config
    from Cryptographer import LoadConfig, LoadFileTypes, resource_path

    # Lang Configuration
    config, lang = LoadConfig()
    fileTypes = LoadFileTypes(lang)


    img1 = ImageTk.PhotoImage(Image.open(resource_path('UI/Loaded.ico')).resize((40, 40)))
    img2 = ImageTk.PhotoImage(Image.open(resource_path('UI/NotLoaded.ico')).resize((40, 40)))

    # Key Input
    if config['State']['keyfile'] != 'None':
        key = config['State']['keyfile']
        Indicator = Label(KeyFrame, image=img1) # LoadIndicator 
        IndicatorTooltip = ToolTip(Indicator, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['Loaded'], delay=1.0) # Tooltip for LoadIndicator
    else:
        key = ''
        Indicator = Label(KeyFrame, image=img2) # LoadIndicator
        IndicatorTooltip = ToolTip(Indicator, msg=lang.Main['IndicatorTooltip'] + lang.Dialog['NotLoaded'], delay=1.0) # Tooltip for LoadIndicator
    Indicator.grid(row=0, column=1, rowspan=2, padx=5)
    Button(KeyFrame, text=lang.Main['BrowseKeyBtn'], command=lambda: BrowseKeyDialog(KeyFrame)).grid(row=0, column=0, pady=2)
    Button(KeyFrame, text=lang.Main['GenerateKeyBtn'], command=GenerateKey).grid(row=1, column=0, padx=10, pady=6)
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