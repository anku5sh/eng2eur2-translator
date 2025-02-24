@echo off
.venv\Scripts\activate
pyinstaller --noconfirm --onefile --windowed ^
  --name "Eng2Eur2" ^
  --add-data "src;src" ^
  --hidden-import PyQt6 ^
  --hidden-import deep_translator ^
  src/main.py
