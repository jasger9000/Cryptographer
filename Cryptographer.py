from tkinter import filedialog, messagebox, Tk, Label, Button, Entry, LabelFrame
from cryptography.fernet import Fernet, InvalidToken
from pathlib import Path
import logging
from os.path import expandvars, getsize



# logger config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fmt = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')

# fileHandler config
fileHandler = logging.FileHandler('Cryptographer.log')
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(fmt)
logger.addHandler(fileHandler)

# streamHandler config
debug = True
if debug is True:
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(fmt)
    streamHandler.setLevel(logging.DEBUG)
    logger.addHandler(streamHandler)

with open('Cryptographer.log', 'w') as f:
    f.write('')

textFiles = '*.txt', '*.doc', '*.docx', '*.log', '*.msg', '*.odt', '*.pages', '*.rtf', '*.tex', '*.wpd', '*.wps'
audioFiles = '*.aif', '*.aiff', '*.iff', '*.m3u', '*.m4a', '*.mp3', '*.mpa', '*.wav', '*.wma', '*.aup3', '*.aup', '*.ogg', '*.mp2'
videoFiles = '*.mp4', '*.mov', '*.avi', '*.flv', '*.mkv', '*.wmv', '*.avchd', '*.webm', '*MPEG-4', '*.H.264'
version = 'ver. 1.0.0'
logger.info(f'Running Symmetric Cryptographer {version}')


def BrowseKeyDialog(keyEntry):
    browseKeyDialog = filedialog.askopenfilename(initialdir=expandvars(R'C:\Users\$USERNAME\Documents'), title='Open Key...', filetypes=(('Key files', '*.key'),('All files', '*.*')))
    if browseKeyDialog:
        logger.info('User selected key')
        keyEntry.delete(0,"end")
        keyEntry.insert(0, browseKeyDialog)
    return

def BrowseEncryptDialog(encrypt2Entry):
    global textFiles
    browseEncryptDialog = filedialog.askopenfilename(initialdir=expandvars(R'C:\Users\$USERNAME\Documents'), title=f'Select file to Encrypt...', filetypes=(('Text files', textFiles), ('Audio files', audioFiles), ('Video files', videoFiles),('Pdf files', '*.pdf'), ('All files', '*.*')))
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
    if mode == 'Encrypt':
        filePath = entry.get()
    elif mode == 'Decrypt':
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
                    
                    logger.info(f'imports fileContents in Cryptography2 {mode} mode')
                    # imports fileContents of file to encrypt
                    # TODO Fix video and audio encrypting
                    with open(filePath, 'r') as f:
                        fileContents = f.read()

                    # Checks if / or \ is used
                    if filePath.find('/') != -1:
                        seperator = '/'
                    elif filePath.find(chr(92)) != -1:
                        seperator = chr(92)
                    # Encrypts or Decrypts the file, creates filePath2 + some other variables and deletes fileContents and filePath out of Memory
                    if mode == 'Encrypt':
                        fileContents = k.encrypt(fileContents.encode()).decode()
                        fileExtention = Path(filePath).suffix
                        pathLength2 = len(filePath.replace(fileExtention, ''))
                        filePath2 = filedialog.asksaveasfilename(initialdir=expandvars(filePath[0:filePath.rfind(seperator) + 1]), defaultextension='.*', initialfile=f'Encrypted {filePath[filePath.rfind(seperator) + 1:pathLength2]}', title='Save Encrypted file...', filetypes=(('Encrypted file', '*.Encrypted'),('Text file', '*.txt'),('Any file', '*.*')))
                        # writes encrypted Contents to file
                        if filePath2:
                            logger.info('Encrypts and saves file')
                            with open(filePath2, 'w') as f:
                                f.write(f'{fileExtention} {fileContents}')
                        else:
                            logger.info('Finished Cryptography2 because User cancelled saving')
                            return
                    elif mode == 'Decrypt':
                        fileContents = fileContents.split(' ')
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
        logger.info(f'shows NoKeyEntered warning in Cryptograph2 {mode} mode')
        messagebox.showwarning(title=f'No {mode}ion Key entered', message=f'Please insert or generate a {mode}ion Key to {mode} the file with!')
    elif len(filePath) == 0:
        logger.info(f'shows NoMessageEntered warning in Cryptograph2 {mode} mode')
        messagebox.showwarning(title='No filepath entered', message=f'Please enter a filepath of the file to {mode}!')
    return

def Copy(root, out):
    try:
        root.clipboard_clear()
        root.clipboard_append(out.get())
    except Exception:
        logger.exception(f'Unknown error/uncaught exception in Copy()')
        messagebox.showerror(title='Unknown error', message=f'An unknown error occurred while trying to copy!')
    return


def main():
    # GUI Configuration
    root = Tk()
    root.title(f'Cryptographer {version}')
    root.iconbitmap('Cryptographer.exe')
    root.geometry('739x325')
    root.resizable(0,0)
    logger.info('loaded Tk Config')

    # Key Input
    Label(root, text='En-/Decryption Key:', font='Helvetica, 14').place(x=270, y=2) # KeyLabel
    Button(root, text='Generate Key', command=lambda: GenerateKey(keyEntry)).place(x=129, y=30) # GenerateKeyBtn
    keyEntry = Entry(root, width=27, font=('Arial', 14)) # Define keyEntry
    keyEntry.place(x=209, y=30) # Put keyEntry on screen
    Button(root, text='Browse', command=lambda: BrowseKeyDialog(keyEntry)).place(x=509, y=30) # BrowseKeyBtn
    logger.info('loaded key input')

    # Encryption frame
    frame1 = LabelFrame(root, text='Encrypt', font=('Arial', 12), padx=10, pady=12)
    frame1.grid(row=0, column=0, padx=10, pady=70)

    # Encrypt option 1
    Label(frame1, text='Encrypt a message:').grid(row=0, column=0) # Description Label
    encrypt1Entry = Entry(frame1, font=('Arial', 14), width=20) # Define Entry
    encrypt1Entry.grid(row=1, column=0) # Put Entry on screen
    Button(frame1, text='Encrypt', command=lambda: Cryptography1('Encrypt', encrypt1Entry, keyEntry, out)).grid(row=1, column=1) # Encrypt Btn

    # Encrypt option 2
    Label(frame1, text='\n\nEncrypt a file:').grid(row=2, column=0) # Description Label
    encrypt2Entry = Entry(frame1, font=('Arial', 14), width=20) # Define Entry
    encrypt2Entry.grid(row=3, column=0) # Put Entry on screen
    Button(frame1, text='Encrypt', command=lambda: Cryptography2('Encrypt', encrypt2Entry, keyEntry, out)).grid(row=3,column=1) # Encrypt Btn
    Button(frame1, text='Browse', command=lambda: BrowseEncryptDialog(encrypt2Entry)).grid(row=3, column=2) # BrowseCryptographyDialog
    logger.info('loaded encrypt options')

    # Decryption Frame
    frame2 = LabelFrame(root, text='Decrypt', font=('Arial', 12), padx=10, pady=12)
    frame2.grid(row=0, column=1, padx=10, pady=70)

    # Decrypt option 1
    Label(frame2, text='Decrypt a message:').grid(row=0, column=0) # Description Label
    decrypt1Entry = Entry(frame2, font=('Arial', 14), width=20) # Define Entry
    decrypt1Entry.grid(row=1, column=0) # Put Entry on screen
    Button(frame2, text='Decrypt', command=lambda: Cryptography1('Decrypt', decrypt1Entry, keyEntry, out)).grid(row=1, column=1) # Decrypt Btn

    # Decrypt option 2
    Label(frame2, text='\n\nDecrypt a file:').grid(row=2, column=0) # Description Label
    decrypt2Entry = Entry(frame2, font=('Arial', 14), width=20) # Define Entry
    decrypt2Entry.grid(row=3, column=0) # Put Entry on screen
    Button(frame2, text='Decrypt', command=lambda: Cryptography2('Decrypt', decrypt2Entry, keyEntry, out)).grid(row=3,column=1) # Decrypt Btn
    Button(frame2, text='Browse', command=lambda: BrowseDecryptDialog(decrypt2Entry)).grid(row=3, column=2) # BrowseDecryptDialog
    logger.info('loaded decrypt options')

    #Output
    Label(root, text='Output:', font='Helvetica, 14').place(x=335, y=260)
    out = Entry(root, font=('Arial', 14), width=27, state='readonly') # Define Entry
    out.place(x=205 , y=290) # Put Entry on screen
    Button(root, text='Copy', command=lambda: Copy(root, out)).place(x=505, y=290)
    logger.info('loading complete')

    root.mainloop()

if __name__ == '__main__':
    main()
