import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from functions import create_soup


class newsUi(QWidget):
    def __init__(self):
        super(newsUi, self).__init__()
        uic.loadUi("News.ui", self)

        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["제목", "링크"])
        self.tableWidget.setColumnWidth(0, self.width() * 6 / 10)
        self.tableWidget.setColumnWidth(1, self.width() * 4 / 10)
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setRowCount(5)
        self.tableWidget_2.setHorizontalHeaderLabels(["제목", "링크"])
        self.tableWidget_2.setColumnWidth(0, self.width() * 6 / 10)
        self.tableWidget_2.setColumnWidth(1, self.width() * 4 / 10)

        def scrape_headline_news():
            print("[오늘의 헤드라인 뉴스]")
            count = 0
            rowcount = 0
            url = "https://news.naver.com"
            soup = create_soup(url)
            news_list = soup.find(
                "ul", attrs={"class": "hdline_article_list"}).find_all("li", limit=5)
            for index, news in enumerate(news_list):
                title = news.find("a").get_text().strip()
                link = url + news.find("a")["href"]
                self.tableWidget.setItem(count, rowcount, QTableWidgetItem(title))
                self.tableWidget.setItem(count, rowcount + 1, QTableWidgetItem(link))
                count += 1
            print()

        def scrape_it_news():
            print("[IT 뉴스]")
            count = 0
            rowcount = 0
            url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230"
            soup = create_soup(url)
            news_list = soup.find("ul", attrs={"class": "type06_headline"}).find_all(
                "li", limit=5)
            for index, news in enumerate(news_list):
                a_idx = 0
                img = news.find("img")
                if img:
                    a_idx = 1  # img 태그가 있으면 1번째 a 태그의 정보를 사용(기사 링크)

                a_tag = news.find_all("a")[a_idx]
                title = a_tag.get_text().strip()
                link = a_tag["href"]
                self.tableWidget_2.setItem(count, rowcount, QTableWidgetItem(title))
                self.tableWidget_2.setItem(count, rowcount + 1, QTableWidgetItem(link))
                count += 1

        scrape_headline_news()
        scrape_it_news()

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    news = newsUi()
    sys.exit(app.exec_())