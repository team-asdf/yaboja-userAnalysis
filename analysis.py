from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool


class Analysis:
    def __init__(self, username):
        self.url = ["https://github.com/" + username + "?tab=repositories", "https://github.com/" + username + "?tab=stars"]
        # self.repo = "https://github.com/" + username + "?tab=repositories"
        # self.star = "https://github.com/" + username + "?tab=stars"
        self.language_dic = {}

    def analyze(self, main_url):
        req = requests.get(main_url)
        while True:
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            languages = soup.find_all("span", {"itemprop": "programmingLanguage"})
            for each in list(languages):
                language = each.text.lstrip().rstrip()
                if language not in self.language_dic:
                    self.language_dic[language] = 1
                else:
                    self.language_dic[language] += 1
            if soup.find("span", {"class": "disabled"}) is None:
                print("Next Page")
                url = str(soup.find("a", string="Next")).split("href=\"")[1].split("\" rel")[0]
                req = requests.get(url)
            elif soup.find("span", {"class": "disabled"}).text == "Next":
                print("Last Page")
                break
            else:
                print("Next Page")
                url = str(soup.find("a", string="Next")).split("href=\"")[1].split("\" rel")[0]
                req = requests.get(url)
        return self.language_dic


def print_dic(dic):
    sorted_dic = sorted(dic, key=dic.get, reverse=True)
    for i in range(len(sorted_dic)):
        print(str(i + 1) + ":", sorted_dic[i])


if __name__ == "__main__":
    s = Analysis("noirbizarre")
    pool = Pool(processes=4)
    temp = pool.map(s.analyze, s.url)
    print_dic(temp[0])
