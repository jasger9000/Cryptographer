import os
Language = 'Deutsch'
version = 1
# if there is a '$'' in a key it stands for a variable and needs to be placed at the position, where the var should be in the final text 


fileTypes = {
    'Text': 'Text Dateien',
    'Video': ' Video Dateien',
    'Audio': 'Audio Dateien',
    'Picture': 'Bild Dateien',
    'All': 'Alle Dateien',
    'Encrypted': 'Verschlüsselte Dateien',
    'Key': 'Schlüssel Dateien',
    'PrivateKey': 'Privatschlüssel Dateien',
    'PublicKey': 'Öffentlich-Schlüssel Dateien'# needs better translation
}
Dialog = {
    'Open': 'Wählen Sie ',
    'Save': 'Speichern ',
    'file': 'Datei',
    'to': 'zum',
    'Encrypt': 'Verschlüsseln',
    'Encryption': 'Verschlüsselung',
    'Encrypted': 'Verschlüsselt',
    'Decrypt': 'Entschlüsseln',
    'Decryption': 'Entschlüsselung',
    'Decrypted': 'Entschlüsselt',
    'Key': 'Schlüssel',
    'Private': 'Privatschlüssel',
    'Public': 'Öffentlichen Schlüssel',
    'Loaded': 'Geladen',
    'NotLoaded': 'Nicht geladen',
    'Finish': 'Neustarten'
}
Messages = {
    'NoNewLang': 'Keine Sprachen verfügbar',
    'TooBigTitle': 'Datei zu groß',
    'TooBigMessage1': 'Bei Dateien, die größer als 100mb sind, dauert das $ länger.\nMöchten Sie trotzdem fortfahren?',
    'TooBigMessage2': 'Bei Dateien, die größer als 1 Gigabyte sind, dauert das $ mehrere Minuten, oder schlägt fehl.\nMöchten Sie trotzdem fortfahren?', # $ = Encrypt/Decrypt
    'AbortedKeyTitle': 'Schlüsselgenerierung abgebrochen',
    'AbortedKeyMessage': 'Die Schlüsselgenerierung wurde abgebrochen, weil Sie nur einen Schlüssel generiert haben, Sie aber beide benötigen!',
    'NoTextTitle': 'Keine Nachricht/Datei zum $ angegeben', # $ = encrypt/decrypt
    'NoTextMessage': 'Sie müssen eine Nachricht/einen Dateipfad eingeben, bevor Sie versuchen zu ', # at the end will be Encrypt/Decrypt
    'NoKeyTitle': 'Kein $ eingegeben', # $ = Public key/Private key/Key
    'NoKeyMessage': 'Sie müssen einen $ einfügen, bevor Sie versuchen zu $', # 1.$ = Public key/Private key/Key; 2.$ = encrypt/decrypt
    'WrongKeyTitle': 'Falscher $ eingegeben', # $ = Private key/Key
    'WrongKeyMessage': 'Dies ist der falsche $, um diese Nachricht/Datei zu entschlüsseln! Verwenden Sie den richtigen Schlüssel!', # $ = Private key/Key 
    'KeyNotExistTitle': 'Schlüssel nicht gefunden!',
    'KeyNotExistMessage': "Der $, den Sie verwenden wollten, existiert nicht!\nBitte verwenden Sie einen vorhandenen Schlüssel!", # $ = Private key/Public key/Key
    'TooBigTitle': ' fehlgeschlagen', # first character needs to be empty as there will stand Encryption/Decryption in front
    'TooBigMessage': "Die Nachricht/Datei konnte nicht $ werden, weil sie zu groß war!", # $ = Encrypted/Decrypted
    'ValueTitle': ' fehlgeschlagen', # first character must be empty as there will stand Encryption/Decryption in front
    'ValueMessage': " fehlgeschlagen, da der Dateityp nicht unterstützt wird.", # first character must be empty as there will stand Encryption/Decryption in front
    'fileNotFoundTitle': "Datei nicht gefunden", # lowercase f is intentional
    'fileNotFoundMessage': 'Die Datei, die Sie verwenden möchten, wurde nicht gefunden!\nBitte verwenden Sie eine vorhandene Datei!', # lowercase f is intentional
    'UnknownTitle': 'Unbekannter Fehler',
    'UnknownMessage': f"Es ist ein Unbekannte Fehler aufgetreten.\nBitte öffne ein 'issue' und hängen Sie die Logdatei Ihrer aktuellen Sitzung an.\nGithub: https://github.com/jasger9000/Cryptographer\nLog file: {os.getcwd()}\Cryptographer.log"
}
SettingsLabels = {
    'General': 'Allgemein',
    'AddLangBtn': 'Neu Sprache hinzufügen',
    'LangLabel': 'Sprache',
    'RememberKeyLabel': 'Schlüssel Merken',
    'RememberKeyTip': 'Wenn diese Option aktiviert ist,\nwird der zuletzt verwendete Schlüssel gespeichert\nund bei jedem Start der Software geladen.',
    'AutoCFULabel': 'Beim Start auf Updates prüfen?',

    'Themes': 'Designs',
    'LightTheme': 'Helles Design',
    'DarkTheme': 'Dunkles Design',
    'DefaultBtn': 'Zurücksetzen',
    'ApplyBtn': 'Änderungen übernehmen',
}
NewUpdateTrue = {
    'Title': 'Neue Version verfügbar',
    'Message': "Es steht eine neue Version zum herunterladen bereit.\n Möchten Sie diese installieren?",
}
NewUpdateFalse = {
    'Title1': "Verbindung zum Server konnte nicht hergestellt werden",
    'Message1': "Konnte nicht nach Updates suchen,\Es konnte keine Verbindung zu Github aufgebaut werden.\nBitte versuche es später erneut, oder prüfen Sie, ob Sie mit dem Internet verbunden sind.",
    'Title2': 'Kein Update gefunden',
    'Message2': 'Sie verwenden derzeit die neueste Version dieser Software.',
}
VersionNotFound = {
    'Title': 'Version nicht gefunden!',
    'Message': f"Die Software, die Sie derzeit verwenden, hat keine registrierte Version, bitte installieren Sie die Software erneut.\nWenn Sie dies bereits getan haben, öffnen Sie bitte ein 'Issue' in meinem Github und hänge die log Datei ihrer jetzigen Session an.\nhttps://wwww.github.com/jasger9000/Cryptographer\nLog Datei: {os.getcwd()}\Cryptographer.log"
}
CryptMain = {
    'ModeMenu': 'Modus',
    'ModeSymLabel': 'Symmetrisch',
    'ModeAsymLabel': 'Asymmetrisch',
    
    'HistoryMenu': 'Verlauf',
    
    'HelpMenu': 'Hilfe',
    'HelpGithubLabel': 'Github Seite Öffnen',
    'HelpFilesLabel': 'Installationspfad öffnen',
    'HelpSettingsLabel': 'Einstellungen',
    'SettingsLangLabel': 'Neue Sprache installieren',
    'HelpAboutLabel': 'Über Cryptographer',
    'HelpCFULabel': 'Nach Updates suchen',
    
    'InstallUpdateTitle': 'Installiert Update...',
    'InstallUpdateProgress0': 'Update herunterladen...',
    'InstallUpdateProgress1': 'Update extrahieren...',
    'InstallUpdateProgress2': 'Fertigstellen...',
    'InstallUpdateProgress3': 'Fertiggestellt',
}
# Main is primarily for symmetric mode, but also used for asymmetric mode
Main = {
    'title': 'Symmetrischer Cryptographer',
    'KeyTitle': 'Schlüssel',
    'GenerateKeyBtn': 'Schlüssel generieren',
    'BrowseBtn': 'Durchsuchen',
    'BrowseKeyBtn': 'Schlüssel laden',
    'IndicatorTooltip': 'Zeigt an, ob ein Schlüssel geladen wurde.\nStatus: ', # after space will loaded/not loaded stand
    'Encrypt': 'Verschlüsseln',
    'Decrypt': 'Entschlüsseln',
    'Encrypt1Title': '\nVerschlüssel eine Nachricht:',
    'Encrypt2Title': '\n\nVerschlüssel eine Datei:',
    'Decrypt1Title': '\nEntschlüssel eine Nachricht:',
    'Decrypt2Title': '\n\nEntschlüssel eine Datei:',
    'OutputTitle': 'Output',
    'DeleteBtn': 'Löschen',
    'CopyBtn': 'Kopieren'
}
AsymMain = {
    'title': 'Asymmetrischer Cryptographer',
    'KeysTitle': 'Schlüssel',
    'PublicKeyTitle': 'Öffentlicher Schlüssel:',
    'PrivateKeyTitle': 'Privater Schlüssel:',
    'GenerateKeyBtn': 'Schlüsselpaar Generieren'
}