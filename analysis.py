from github import Github
import time
import sys
import requests


class Analysis:
    def __init__(self, username):
        f = open("/Users/ghyeon/Documents/token/token")
        token = f.readline().rstrip()
        self.github = Github(token)
        f.close()
        self.username = username
        # self.user_text = open("./users/" + username, 'w')
        self.user = self.github.get_user(username)
        self.lang_dic = {}

    def analysis(self):
        start = time.time()
        print(start)
        # Get Repos
        for each in self.user.get_repos():
            if time.time() - start >= 30:
                return
            if each.language is not None:
                print("Repo:", each.language)
                if each.language == "C":
                    pass
                elif each.language not in self.lang_dic:
                    self.lang_dic[each.language] = 2.5
                else:
                    self.lang_dic[each.language] += 2.5

        # Get Starred
        for each in self.user.get_starred():
            print("Star:", each.language)
            if time.time() - start >= 30:
                return
            if each.language is not None:
                if each.language == "C":
                    pass
                elif each.language not in self.lang_dic:
                    self.lang_dic[each.language] = 1.5
                else:
                    self.lang_dic[each.language] += 1.5

        # Get Following
        following = []
        for each in self.user.get_following():
            following.append(self.parse_id(str(each)))

        for username in following:
            temp_user = self.github.get_user(username)
            for each in temp_user.get_repos():
                print("Follow:", each.language)
                if time.time() - start >= 30:
                    return
                if each.language is not None:
                    if each.language == "C":
                        pass
                    elif each.language not in self.lang_dic:
                        self.lang_dic[each.language] = 0.5
                    else:
                        self.lang_dic[each.language] += 0.5

    def parse_id(self, data):
        data = data.split("login=\"")[1].split("\")")[0]
        return data

    def main(self):
        self.analysis()
        languages = sorted(self.lang_dic, key=self.lang_dic.get, reverse=True)
        lang_str = ""
        try:
            for i in range(3):
                lang_str += languages[i]
                if i != 2:
                    lang_str += ","
        except IndexError:
            pass
        try:
            if lang_str[-1] == ",":
                lang_str = lang_str[:-1]
        except IndexError:
            pass
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'userid': self.username,
            'extract_language': lang_str,
            'keyword': ''
        }
        print(lang_str)
        response = requests.post('http://angelbeats.tk:3000/api/v1/signup', headers=headers, data=data)
        # print(response.status_code, response.reason)
        # self.user_text.write(lang_str)
        # self.user_text.close()
        return languages


if __name__ == "__main__":
    start = time.time()
    if len(sys.argv) == 2:
        name = sys.argv[1]
    else:
        name = input()
    s = Analysis(name)
    dic = s.main()
    print(s.lang_dic)
    print("Elapsed Time:", time.time() - start)
