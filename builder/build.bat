pyinstaller -i CryptographerIcon.ico --onefile -w python\Cryptographer.py
move dist\Cryptographer.exe executables
del /Q /S python\__pycache__ Cryptographer.spec build
RMDIR /Q /S python\__pycache__ build\Cryptographer build dist 