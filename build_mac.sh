#!/bin/zsh
source .venv/bin/activate

TCL_TK_PREFIX=$(brew --prefix tcl-tk)

pyinstaller --noconfirm --windowed \
  --name "eng2eur2" \
  --add-data "src:src" \
  --hidden-import PyQt6 \
  --hidden-import deep_translator \
  --collect-submodules "tkinter" \
  --paths "$TCL_TK_PREFIX/lib" \
  --runtime-hook <(echo "import os; os.environ['TCL_LIBRARY'] = '$TCL_TK_PREFIX/lib/Tcl.framework/Versions/8.6/Resources/Scripts/tcl8.6'; os.environ['TK_LIBRARY'] = '$TCL_TK_PREFIX/lib/Tk.framework/Versions/8.6/Resources/Scripts/tk8.6'") \
  src/main.py
