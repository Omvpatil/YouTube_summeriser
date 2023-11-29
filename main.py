import sys,os
import openai
from config import OPENAI_API_KEY
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit,
                             QSplitter, QHBoxLayout, QVBoxLayout, QStatusBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from transcriber import get_video_transcript, summarize_transcript, TranscriptsDisabled


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 700, 700
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowIcon(QIcon('./icon.png'))
        self.setWindowTitle('YouTube Video Summarize App')

        self.setStyleSheet('''
              Widget {
                    font-size: 14 px;
                    }
        ''')

        self.layout = {}
        self.layout['main'] = QVBoxLayout()
        self.setLayout(self.layout['main'])

        self.init_UI()
        self.config_signal()

    def transcribe_video(self):
        video_id = self.video_id_input.text()
        if not video_id:
            self.statusbar.showMessage('Video Id Is Missing')
            return
        self.statusbar.clearMessage()
        self.transcription_field.clear()
        self.summarized_field.clear()

        try:
            transcription = get_video_transcript(video_id)
            self.transcription_field.setPlainText(transcription)
        except TranscriptsDisabled:
            self.statusbar.showMessage('Transcription not available')
        except Exception as e:
            self.statusbar.showMessage(str(e))

    def summarized_video(self):
        transcription = self.transcription_field.toPlainText()
        if not transcription:
            self.statusbar.showMessage('Transcription is empty')
        self.summarized_field.clear()
        self.statusbar.clearMessage()
        try:
            video_summary = summarize_transcript(transcription)
            self.summarized_field.setPlainText(video_summary)
        except Exception as e:
            self.statusbar.showMessage(str(e))

    def init_UI(self):
        # youtube videos ID input
        self.layout['video_id_entry'] = QHBoxLayout()
        self.layout['main'].addLayout(self.layout['video_id_entry'])
        self.video_id_input = QLineEdit()
        self.layout['video_id_entry'].addWidget(QLabel('video ID: '))
        self.layout['video_id_entry'].addWidget(self.video_id_input)
        self.layout['video_id_entry'].addStretch(1)

        splitter = QSplitter(Qt.Orientation.Vertical)
        self.layout['main'].addWidget(splitter)

        # insert input and output textbox
        self.transcription_field = QTextEdit()
        self.summarized_field = QTextEdit()
        splitter.addWidget(self.transcription_field)
        splitter.addWidget(self.summarized_field)

        # prevent splitter to be completely closed
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)

        # add buttons
        self.layout['button'] = QHBoxLayout()
        self.layout['main'].addLayout(self.layout['button'])

        self.btn_transcribe = QPushButton('&Transcribe')
        self.btn_transcribe.setFixedWidth(250)
        self.btn_summarize = QPushButton('&Summarize')
        self.btn_summarize.setFixedWidth(150)
        self.btn_reset = QPushButton('&Reset')
        self.btn_reset.setFixedWidth(150)
        self.layout['button'].addWidget(self.btn_transcribe)
        self.layout['button'].addWidget(self.btn_summarize)
        self.layout['button'].addWidget(self.btn_reset)
        self.layout['button'].addStretch()

        # add status bar
        self.statusbar = QStatusBar()
        self.layout['main'].addWidget(self.statusbar)

    def reset_fields(self):
        self.video_id_input.clear()
        self.transcription_field.clear()
        self.summarized_field.clear()
        self.statusbar.clearMessage()

    def config_signal(self):
        self.btn_transcribe.clicked.connect(self.transcribe_video)
        self.btn_summarize.clicked.connect(self.summarized_video)
        self.btn_reset.clicked.connect(self.reset_fields)

    if __name__ == '__main__':
        API_key = os.getenv("api_key")
        openai.api_key = API_key

        app = QApplication(sys.argv)

myApp = MyApp()
myApp.show()

try:
    sys.exit(myApp.app.exec())
except SystemExit:
    print('Closing Window....')

