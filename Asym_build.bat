pyinstaller -i CryptographerIcon.ico --onefile -w Asym_Cryptographer.py
move dist\Asym_Cryptographer.exe ..\Cryptographer
del /Q /S __pycache__ Asym_Cryptographer.spec build
RMDIR /Q /S __pycache__ build\Asym_Cryptographer build dist 