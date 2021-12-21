import requests
from bs4 import BeautifulSoup
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import urllib.request
import webbrowser


# 클래스 부분
class netflixUi(QWidget):
    url = "https://top10.netflix.com/south-korea"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(15)
        self.setLayout(grid)
        self.move(800, 0)

        self.link_list = []
        self.hrefbutton = [x for x in range(5)]  # 버튼 리스트(따로 만들어 5위까지 각자 링크 부여해주기 위함)
        for i in range(5):
            image = self.soup.find("button", attrs={"aria-label": "{} of 10".format(i + 1)})
            imgadrs = image.find("img", attrs={"class": "absolute top-0 left-0 object-cover wh-full banner-image"})[
                "src"]
            imgdata = urllib.request.urlopen(imgadrs).read()

            filmhref = \
            image.find("a", attrs={"class": "block text-13px md:text-18px whitespace-nowrap hover:text-white"})["href"]
            filmurl = "{}".format(filmhref)  # url 중간에 kr이 빠져 제목이 영어로 출력됨
            filmres = requests.get(filmurl)
            filmres.raise_for_status()
            filmsoup = BeautifulSoup(filmres.text, "lxml")
            filmtitle = filmsoup.find("h1", attrs={"class": "title-title"}).get_text()

            self.link_list.append(filmurl)

            self.hrefbutton[i] = QToolButton()  # 링크 들어갈 버튼
            self.hrefbutton[i].setText(filmtitle)
            self.hrefbutton[i].clicked.connect(self.buttonclicked)
            self.hrefbutton[i].setObjectName("{}".format(i + 1))

            label = QLabel()  # 이미지 넣는 곳
            thumbnail = QPixmap()
            thumbnail.loadFromData(imgdata)
            scaledtn = thumbnail.scaledToWidth(250)
            label.setPixmap(scaledtn)
            grid.addWidget(label)
            grid.addWidget(self.hrefbutton[i])

        self.show()

    def buttonclicked(self):
        button = self.sender()
        name = button.objectName()

        for j in range(1, 6):
            if name == "{}".format(j):
                webbrowser.open(self.link_list[j - 1])


# 이벤트 루프
if __name__ == "__main__":
    app = QApplication(sys.argv)
    netflix = netflixUi()
    sys.exit(app.exec_())