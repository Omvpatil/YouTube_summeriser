import sys,os
import openai
from PyQt6.QtWidgets import (QApplication,QWidget,QPushButton,QLabel,QLineEdit,QTextEdit,
                             QSplitter,QHBoxLayout,QVBoxLayout,QStatusBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon,QFont
from transcriber import get_video_transcript,summarize_transcript,TranscriptsDisabled

def resource_path(relative_path):
        try:
            base_path= sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

API_key = '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'