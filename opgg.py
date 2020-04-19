import requests
from bs4 import BeautifulSoup
import csv


class Scraper():
    def __init__(self):
        self.url = "https://www.op.gg/ranking/ladder/page="

    def getHTML(self, cnt):
        res = requests.get(self.url + str(cnt+1))
        if res.status_code != 200:
            print("request error : ", res.status_code)

        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        return soup

    def userInfo(self, soup, cnt):
        userInformation = soup.find_all("tr", class_="ranking-table__row")
        userNamelst = soup.select("tr td a span")

        userRank = []
        userTier = []
        userLP = []
        userName = []

        if cnt == 0:
            topUserInfo = soup.find_all("li", class_="ranking-highest__item")

            for k in topUserInfo:
                if k.find("div", class_="ranking-highest__rank") is not None:
                    userRank.append(k.find("div", class_="ranking-highest__rank").text.strip())
                if k.select(".ranking-highest__tierrank > span") is not None:
                    userTier.append(k.select(".ranking-highest__tierrank > span")[0].text.strip())
                if k.select(".ranking-highest__tierrank > b") is not None:
                    userLP.append(k.select(".ranking-highest__tierrank > b")[0].text.strip())

                for m in k.find_all("a", class_="ranking-highest__name"):
                    userName.append(m.text)

        for j in userInformation:
            if j.find("td", class_="ranking-table__cell ranking-table__cell--rank") is not None:
                userRank.append(j.find("td", class_="ranking-table__cell ranking-table__cell--rank").text.strip())
            if j.find("td", class_="ranking-table__cell ranking-table__cell--tier") is not None:
                userTier.append(j.find("td", class_="ranking-table__cell ranking-table__cell--tier").text.strip())
            if j.find("td", class_="ranking-table__cell ranking-table__cell--lp") is not None:
                userLP.append(j.find("td", class_="ranking-table__cell ranking-table__cell--lp").text.strip())

        for i in userNamelst:
            userName.append(i.text)

        self.writeCSV(userRank, userTier, userLP, userName)

    def writeCSV(self, rank, tier, lp, name):
        file = open("opgg.csv", "a", encoding='UTF-8', newline="")

        wr = csv.writer(file)
        for i in range(len(rank)):
            wr.writerow([rank[i], tier[i], lp[i], name[i]])

    def scrap(self):

        file = open("opgg.csv", "w", newline="")
        wr = csv.writer(file)
        wr.writerow(["Rank", "Tier", "LP", "Name"])
        file.close()

        for i in range(5):
            soup = self.getHTML(i)
            self.userInfo(soup, i)


if __name__ == "__main__":
    s = Scraper()
    s.scrap()
