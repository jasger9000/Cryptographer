pyinstaller -i CryptographerIcon.ico --onefile -w python\Sym_Cryptographer.py
move dist\Sym_Cryptographer.exe executables
del /Q /S python\__pycache__ Sym_Cryptographer.spec build
RMDIR /Q /S python\__pycache__ build\Sym_Cryptographer build dist 