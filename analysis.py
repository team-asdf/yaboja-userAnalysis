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
                # print(language)
            next_button = soup.find_all("a", {"rel": "nofollow"})
            no_next = True
            for each in next_button:
                if each is not None and each.text == "Next":
                    no_next = False
            if no_next:
                print("Last Page")
                break
            else:
                print("Next Page")
                url = str(soup.find("a", string="Next")).split("href=\"")[1].split("\" rel")[0]
                req = requests.get(url)
        return self.language_dic


def print_dic(lst):
    dic = {}
    for l in lst:
        for each in l:
            if each in dic:
                dic[each] += l[each]
            else:
                dic[each] = l[each]
    sorted_dic = sorted(dic, key=dic.get, reverse=True)
    for i in range(len(sorted_dic)):
        print(str(i + 1) + ":", sorted_dic[i])


if __name__ == "__main__":
    import time
    start = time.time()
    s = Analysis("seongjoojin")
    pool = Pool(processes=4)
    temp = pool.map(s.analyze, s.url)
    # print(temp)
    print_dic(temp)
    print(time.time() - start)
