import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from functions import create_soup
import re
import requests
from bs4 import BeautifulSoup



class conversationUi(QDialog):
    def __init__(self):
        super(conversationUi, self).__init__()
        uic.loadUi("conversation.ui", self)


        def scrape_today_english():

            print("[오늘의 영어 회화]")
            url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english#;"
            soup = create_soup(url)
            sentences = soup.find_all("div", attrs={"id": re.compile("^conv_kor_t")})
            todaysExpression = soup.find_all("b", attrs={"class": "conv_txtTitle"})
            print()
            print("(영어 지문)")
            # 8문장이 있다고 가정할 때, index 기준 4~7까지 잘라서 가져오면 된다.
            print("<Today's expression>")
            print(todaysExpression[1].get_text())
            print()
            self.english_widget.addItem("<Today's expression>")

            for sentence in sentences[len(sentences)//2:]:
                complete_sentence = sentence.get_text().strip()
                self.english_widget.addItem(complete_sentence)
                print(sentence.get_text().strip())
            # 8문장이 있다고 가정할 때, index 기준 0~3까지 잘라서 가져오면 된다.
            print()
            print("(한글 지문)")
            print("<오늘의 표현>")
            print(todaysExpression[0].get_text())
            print()
            self.korean_widget.addItem("<오늘의 표현>")
            for sentence in sentences[:len(sentences)//2]:
                complete_sentence = sentence.get_text().strip()
                self.korean_widget.addItem(complete_sentence)
                print(sentence.get_text().strip())
            print()

        scrape_today_english()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    conversation = conversationUi()
    sys.exit(app.exec_())