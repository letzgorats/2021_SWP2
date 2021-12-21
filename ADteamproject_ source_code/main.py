import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.uic.uiparser import QtWidgets
from netflix import netflixUi
from youtube import youtubeUi
from news import newsUi
from conversation import conversationUi
from img import img

# widget index 0: 메인
# widget index 1: 영화추천버튼위젯
# widget index 2: 넷플릭스
# widget index 3: 유튜브
# widget index 4: 뉴스
# widget index 5: 영어/한글 회화


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("Main.ui", self)
        self.movie_button.clicked.connect(self.openbuttonWindowClass)
        self.news_button.clicked.connect(self.openNews)
        self.english_button.clicked.connect(self.openConversation)

    def openbuttonWindowClass(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def openNews(self):
        widget.setCurrentIndex(widget.currentIndex() + 4)

    def openConversation(self):
        widget.setCurrentIndex(widget.currentIndex() + 5)


class MovieSelectButtonWindow(QWidget):
    def __init__(self):
        super(MovieSelectButtonWindow, self).__init__()
        uic.loadUi("movieselectbutton.ui", self)
        self.go_to_netflix.clicked.connect(self.openNetflixClass)
        self.go_to_youtube.clicked.connect(self.openYoutubeClass)
        self.go_to_home.clicked.connect(self.openMainClass)

    def openNetflixClass(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def openYoutubeClass(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)

    def openMainClass(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = QStackedWidget()

    mainWindow = MainWindow()
    netflixWindow = netflixUi()
    youtubeWindow = youtubeUi()
    newsWindow = newsUi()
    conversationWindow = conversationUi()
    movieselectbuttonWindow = MovieSelectButtonWindow()

    widget.addWidget(mainWindow)
    widget.addWidget(movieselectbuttonWindow)
    widget.addWidget(netflixWindow)
    widget.addWidget(youtubeWindow)
    widget.addWidget(newsWindow)
    widget.addWidget(conversationWindow)

    widget.show()

    app.exec_()