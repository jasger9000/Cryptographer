pyinstaller -i CryptographerIcon.ico --onefile -w python\Asym_Cryptographer.py
move dist\Asym_Cryptographer.exe executables
del /Q /S python\__pycache__ Asym_Cryptographer.spec build
RMDIR /Q /S python\__pycache__ build\Asym_Cryptographer build dist 