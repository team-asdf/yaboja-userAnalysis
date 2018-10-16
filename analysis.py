from bs4 import BeautifulSoup
import requests


class Analysis:
    def __init__(self, username):
        self.repo = "https://github.com/" + username + "?tab=repositories"
        self.star = "https://github.com/" + username + "?tab=stars"

    def analyze(self):
        language_dic = {}
        # Repository
        req = requests.get(self.repo)
        while True:
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            languages = soup.find_all("span", {"itemprop": "programmingLanguage"})
            for each in list(languages):
                language = each.text.lstrip().rstrip()
                if language not in language_dic:
                    language_dic[language] = 1
                else:
                    language_dic[language] += 1
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

        # Star
        req = requests.get(self.star)
        while True:
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            languages = soup.find_all("span", {"itemprop": "programmingLanguage"})
            for each in list(languages):
                language = each.text.lstrip().rstrip()
                if language not in language_dic:
                    language_dic[language] = 1
                else:
                    language_dic[language] += 1
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

        print(language_dic)
        print(sorted(language_dic, key=language_dic.get, reverse=True))


if __name__ == "__main__":
    s = Analysis("jen6")
    s.analyze()
