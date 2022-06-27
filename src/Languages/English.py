import os
Language = 'English'
# if there is a '$'' in a key it stands for a variable and needs to be placed at the position, where the var should be in the final text 


fileTypes = {
    'Text': 'Text files',
    'Video': ' Video files',
    'Audio': 'Audio files',
    'Picture': 'Picture files',
    'All': 'All files',
    'Encrypted': 'Encrypted files',
    'Key': 'Key files',
    'PrivateKey': 'Private key files',
    'PublicKey': 'Public key files'
}
Dialog = {
    'Open': 'Select ',
    'Save': 'Save ',
    'file': 'file',
    'to': ' to ',
    'Encrypt': 'Encrypt',
    'Encryption': 'Encryption',
    'Encrypted': 'Encrypted',
    'Decrypt': 'Decrypt',
    'Decryption': 'Decryption',
    'Decrypted': 'Decrypted',
    'Key': 'Key',
    'Private': 'Private key',
    'Public': 'Public key',
    'Loaded': 'Loaded',
    'NotLoaded': 'Not loaded',
    'Finish': 'Restart'
}
Messages = {
    'NoNewLang': 'No Languages available',
    'TooBigTitle': 'file too big',
    'TooBigMessage1': 'Files larger than 100mb could take a longer time to $.\nWould you still like to proceed?', # $ = Encrypt/Decrypt
    'TooBigMessage2': 'Files larger than 1 Gigabyte will take several minutes to $ or will fail.\nWould you still like to proceed?', # $ = Encrypt/Decrypt
    'AbortedKeyTitle': 'Aborted Key Generation',
    'AbortedKeyMessage': 'Key generation aborted because you only tried to generate one key, but you need both!',
    'NoTextTitle': 'No message to $ entered', # $ = encrypt/decrypt
    'NoTextMessage': 'You need to enter a message/filepath before you try to ', # at the end will be Encrypt/Decrypt
    'NoKeyTitle': 'No $ entered', # $ = Public key/Private key/Key
    'NoKeyMessage': 'You need to insert a $ before you try to $', # 1.$ = Public key/Private key/Key; 2.$ = encrypt/decrypt
    'WrongKeyTitle': 'Wrong $ entered!', # $ = Private key/Key
    'WrongKeyMessage': 'This is the wrong $ to decrypt this message/file! Use the right Key!', # $ = Private key/Key 
    'KeyNotExistTitle': 'Key not found',
    'KeyNotExistMessage': "The $ you tried to use does not exist!\nPlease use an existing Key!", # $ = Private key/Public key/Key
    'TooBigTitle': ' failed', # first character needs to be empty as there will stand Encryption/Decryption in front
    'TooBigMessage': "The message/file couldn't be $ because it was too big!", # $ = Encrypted/Decrypted
    'ValueTitle': ' failed', # first character must be empty as there will stand Encryption/Decryption in front
    'ValueMessage': "$ failed because the filetype isn't supported", # first character must be empty as there will stand Encryption/Decryption in front
    'fileNotFoundTitle': "File not found", # lowercase f is intentional
    'fileNotFoundMessage': 'The file you would like to use was not found!\nPlease use an existing file!', # lowercase f is intentional
    'UnknownTitle': 'Unknown Error',
    'UnknownMessage': f"An Unknown Error occurred.\nPlease open an issue and attach the log file of your current session.\nGithub: https://github.com/jasger9000/Cryptographer\nLog file: {os.getcwd()}\Cryptographer.log"
}
SettingsLabels = {
    'AddLangBtn': 'Add new Language',
    'LangLabel': 'Language    ',
    'RememberKeyLabel': 'Remember key    ',
    'AutoCFULabel': 'Check for Updates at startup?',
    'DefaultBtn': 'Reset',
    'ApplyBtn': 'Apply Changes',
    'LightTheme': 'Light Theme',
    'DarkTheme': 'Dark Theme',
}
NewUpdateTrue = {
    'Title': 'New version available',
    'Message': "There's a new version available for download.\n Would you like to install it?",
}
NewUpdateFalse = {
    'Title1': "Couldn't connect to server",
    'Message1': "Couldn't check for Updates,\nConnection to Github couldn't be Established.\nPlease try again later or check if you are Connected to the Internet.",
    'Title2': 'No Update found',
    'Message2': 'You are currently running the newest version of this Software.',
}
VersionNotFound = {
    'Title': 'Version not found!',
    'Message': f"The Software you are currently using doesn't have a Version registered to it,\nplease reinstall the Software.\nIf you have already done this,\nPlease open an issue and attach the log file of your current session.\nGithub: https://github.com/jasger9000/Cryptographer\nLog file: {os.getcwd()}\Cryptographer.log"
}
CryptMain = {
    'ModeMenu': 'Mode',
    'ModeSymLabel': 'Symmetric',
    'ModeAsymLabel': 'Asymmetric',
    
    'HistoryMenu': 'History',
    
    'HelpMenu': 'Help',
    'HelpGithubLabel': 'Open Github Page',
    'HelpFilesLabel': 'Open Installation Path',
    'HelpSettingsLabel': 'Settings',
    'SettingsLangLabel': 'Install new Language',
    'HelpAboutLabel': 'About Cryptographer',
    'HelpCFULabel': 'Check for Updates',
    
    'InstallUpdateTitle': 'Installing Update...',
    'InstallUpdateProgress0': 'Downloading Update...',
    'InstallUpdateProgress1': 'Extracting Update...',
    'InstallUpdateProgress2': 'Finishing...',
    'InstallUpdateProgress3': 'Finished',
}
# Main is primarily for symmetric mode, but also used for asymmetric mode
Main = {
    'title': 'Symmetric Cryptographer',
    'KeyTitle': 'Key',
    'GenerateKeyBtn': 'Generate key',
    'BrowseBtn': 'Browse',
    'BrowseKeyBtn': 'Load Key',
    'IndicatorTooltip': 'Indicates if a key has been loaded.\nStatus: ', # after space will loaded/not loaded stand
    'Encrypt': 'Encrypt',
    'Decrypt': 'Decrypt',
    'Encrypt1Title': '\nEncrypt a message:',
    'Encrypt2Title': '\n\nEncrypt a file:',
    'Decrypt1Title': '\nDecrypt a message:',
    'Decrypt2Title': '\n\nDecrypt a file:',
    'OutputTitle': 'Output',
    'DeleteBtn': 'Delete',
    'CopyBtn': 'Copy'
}
AsymMain = {
    'title': 'Asymmetric Cryptographer',
    'KeysTitle': 'Keys',
    'PublicKeyTitle': 'Public key:',
    'PrivateKeyTitle': 'Private key:',
    'GenerateKeyBtn': 'Generate Keypair'
}