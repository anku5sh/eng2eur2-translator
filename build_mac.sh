#!/bin/zsh
source .venv/bin/activate
pyinstaller --noconfirm --windowed \
  --name "eng2eur2" \
  --add-data "src:src" \
  --hidden-import PyQt6 \
  --hidden-import deep_translator \
  --collect-submodules "tkinter" \
  --runtime-hook <(echo "import os; os.environ['TCL_LIBRARY'] = 'Tcl'; os.environ['TK_LIBRARY'] = 'Tk'") \
  src/main.py
