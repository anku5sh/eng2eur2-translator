import sys
import asyncio
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QProgressBar
)
from PyQt6.QtCore import pyqtSignal, QObject
from deep_translator import GoogleTranslator

LANGUAGES = [
    'BG', 'CS', 'DA', 'DE', 'EL', 'ES', 'ET', 'FI', 'FR', 'HU',
    'IT', 'LT', 'LV', 'NL', 'PL', 'PT', 'RO', 'SK', 'SL', 'SV'
]

class Translator(QObject):
    translation_done = pyqtSignal(str, str, str)  # (lang, text, translation)

class TranslationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eng2Eur2 Translator")
        self.setGeometry(100, 100, 800, 600)
        self.translator = Translator()
        self.init_ui()

    def init_ui(self):
        # Widget setup (unchanged from previous)
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.input_label = QLabel("Enter phrases (semicolon-separated):")
        self.input_field = QLineEdit()
        self.translate_btn = QPushButton("Translate")
        self.progress_bar = QProgressBar()
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)

        layout.addWidget(self.input_label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.translate_btn)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.output_area)

        self.translate_btn.clicked.connect(self.start_translation)
        self.input_field.returnPressed.connect(self.start_translation)
        self.translator.translation_done.connect(self.update_output)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_translation(self):
        text = self.input_field.text().strip()
        if not text:
            return

        self.input_field.clear()
        self.output_area.clear()
        self.progress_bar.setValue(0)

        phrases = [p.strip() for p in text.split(';') if p.strip()]
        asyncio.create_task(self.process_translations(phrases))

    async def process_translations(self, phrases):
        total = len(phrases) * len(LANGUAGES)
        completed = 0

        for phrase in phrases:
            self.output_area.append(f"\nTranslating: {phrase}")
            tasks = []

            for lang in LANGUAGES:
                task = asyncio.create_task(
                    self.translate_phrase(phrase, lang)
                )
                tasks.append(task)

            for task in tasks:
                lang, result = await task
                completed += 1
                self.progress_bar.setValue(int((completed / total) * 100))

    async def translate_phrase(self, phrase, lang):
        try:
            loop = asyncio.get_running_loop()
            translated = await loop.run_in_executor(
                None,
                lambda: GoogleTranslator(
                    source='auto',
                    target=lang.lower()
                ).translate(phrase)
            )
            self.translator.translation_done.emit(lang, phrase, translated)
            return (lang, f"{translated} ({len(translated)} chars)")
        except Exception as e:
            return (lang, f"Error: {str(e)}")

    def update_output(self, lang, original, translation):
        self.output_area.append(f"{lang}: {translation}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslationApp()
    window.show()

    # Integrate asyncio with Qt event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    with loop:
        sys.exit(app.exec())
