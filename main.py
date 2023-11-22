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

class Myapp(Qwidget):
    def __init__(self):
        super()._init_()
        self.window_width,self.window_height = 700, 700
        self.setMinimumsize(self.window_width, self.window_height)
        self.setWindowIcon(QIcon('./icon.png'))
        self.setWindowTitle('YouTube Video Summarize App')

        self.layout = {}
        self.layout['main'] = QVBoxLayout()
        self.setlayout(self.layout['main'])

if __name__ == '__main__':
    API_key = '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'
    openai.api_key = API_key

    app = QApplication(sys.argv)

    qss_style = open(resource_path('dark_orange_style.qss'),'r')
    app.setstylesheet(qss_style.read())

    myApp = MyApp()
    myapp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window....')