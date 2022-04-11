pyinstaller -i CryptographerIcon.ico --onefile -w Sym_Cryptographer.py
move dist\Sym_Cryptographer.exe ..\Cryptographer
del /Q /S __pycache__ Sym_Cryptographer.spec build
RMDIR /Q /S __pycache__ build\Sym_Cryptographer build dist 