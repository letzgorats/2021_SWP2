from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWebEngineWidgets
import sys
import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver


class youtubeUi(QWidget):
    url = "https://www.youtube.com/feed/trending?bp=6gQJRkVleHBsb3Jl"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    options = webdriver.ChromeOptions()  # 창 없이 selenium 실행하는 코드 2줄
    options.add_argument("headless")

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    link_list = []  # 링크 저장할 리스트(buttonclicked 함수에서 사용함)
    button_list = [x for x in range(5)]  # 버튼 리스트(따로 만들어 5위까지 각자 링크 부여해주기 위함)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(15)
        self.setWindowTitle("Youtube")  # 창 제목
        self.move(500, 0)  # 창 초기 위치

        for i in range(5):  # 인기순위 5위까지 출력
            img_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-shelf-renderer/div/div[2]/ytd-expanded-shelf-contents-renderer/div/ytd-video-renderer[{}]/div/ytd-thumbnail/a/yt-img-shadow/img'.format(
                i + 1)
            link_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-shelf-renderer/div/div[2]/ytd-expanded-shelf-contents-renderer/div/ytd-video-renderer[{}]/div/div/div/div/h3/a'.format(
                i + 1)
            image = self.driver.find_element_by_xpath(img_xpath)
            link = self.driver.find_element_by_xpath(link_xpath)

            img_url = image.get_attribute('src')  # 위의 xpath 통해 이미지 소스 추출
            link_url = link.get_attribute('href')  # 위의 xpath 통해 영상 링크 추출
            imgdata = urllib.request.urlopen(img_url).read()  # 이미지 url Qlabel에 넣을 수 있게 데이터화

            self.link_list.append(link_url)

            label = QLabel()  # 유튜브 썸네일
            thumbnail = QPixmap()
            thumbnail.loadFromData(imgdata)
            scaledtn = thumbnail.scaledToWidth(250)  # 썸네일 크기 조정
            label.setPixmap(scaledtn)
            grid.addWidget(label)

            self.button_list[i] = QToolButton()  # 보기 버튼
            self.button_list[i].setText("보기")
            self.button_list[i].clicked.connect(self.buttonclicked)  # callback
            self.button_list[i].setObjectName("{}".format(i + 1))  # buttonclicked 함수에서 사용할 객체 이름
            grid.addWidget(self.button_list[i])

        print(self.link_list)
        self.webview = QtWebEngineWidgets.QWebEngineView()
        grid.addWidget(self.webview, 0, 1, 10, 1)

        self.setLayout(grid)

        self.show()

    def buttonclicked(self):
        button = self.sender()
        name = button.objectName()
        for j in range(1, 6):
            if name == "{}".format(j):  # initUI 보기 버튼에서 설정해준 객체이름이 j(순위)와 같으면
                self.webview.setUrl(QUrl(self.link_list[j - 1]))  # 클래스 초반에 만들어준 링크 리스트를 통해 웹뷰에 순위에 맞는 주소 부여


if __name__ == "__main__":
    app = QApplication(sys.argv)
    youtube = youtubeUi()
    sys.exit(app.exec_())
