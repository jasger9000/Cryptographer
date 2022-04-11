pyinstaller -i CryptographerIcon.ico --onefile -w Cryptographer.py
move dist\Cryptographer.exe ..\Encrypter
del /Q /S __pycache__ Cryptographer.spec build
RMDIR /Q /S __pycache__ build\Cryptographer build dist 