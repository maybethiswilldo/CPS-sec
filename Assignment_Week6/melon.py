from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import csv

path = os.getcwd() + "/chromedriver.exe"
driver = webdriver.Chrome(path)

try:
    driver.get("https://www.melon.com/index.htm")
    time.sleep(1)

    searchIndex = "아이유"
    searchBox = driver.find_element_by_xpath('//*[@id="top_search"]')
    searchBox.send_keys(searchIndex)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="gnb"]/fieldset/button[2]').click()

    driver.find_element_by_xpath('//*[@id="divCollection"]/ul/li[3]/a').click()

    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")

    pages = int(bs.find("div", class_="paginate").find("span", class_="page_num").find_all("a")[-1].text)

    for i in range(2):

        time.sleep(1)

        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")

        title = []
        artist = []
        likes = []

        titleTmp = bs.find_all("a", class_="fc_gray")
        for t in titleTmp:
            title.append(t.text)

        artistTmp = bs.find_all("div", id="artistName")
        for a in artistTmp:
            artistTmp2 = a.select('div > a')
            if len(artistTmp2) > 1:
                artistStr = ""
                for a2 in artistTmp2:
                    artistStr += a2.text
                    if a2 == artistTmp2[-1]:
                        continue
                    else:
                        artistStr += ", "
                artist.append(artistStr)
            elif len(artistTmp2) == 1:
                artist.append(artistTmp2[0].text)

        likesTmp = bs.find_all("span", class_="cnt")
        for like in likesTmp:
            likes.append(like.text[5:])

        file = open("melon.csv", "a", encoding='UTF-8', newline="")
        wr = csv.writer(file)
        for j in range(len(title)):
            wr.writerow([str(j + 1 + (i * 50)), title[j], artist[j], likes[j]])
        file.close()

        driver.find_element_by_xpath('//*[@id="pageObjNavgation"]/div/span/a[{}]'.format(str(i + 1))).click()

finally:
    time.sleep(3)
    driver.quit()
