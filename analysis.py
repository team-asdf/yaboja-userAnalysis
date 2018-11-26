from github import Github
import time
import requests


class Analysis:
    def __init__(self, username):
        f = open("/Users/ghyeon/Documents/token/token")
        token = f.readline().rstrip()
        github = Github(token)
        f.close()
        self.username = username
        self.user_text = open("./users/" + username, 'w')
        self.user = github.get_user(username)
        self.lang_dic = {}

    def analysis(self):
        # Get Repos
        for each in self.user.get_repos():
            if each.language is not None:
                if each.language not in self.lang_dic:
                    self.lang_dic[each.language] = 1
                else:
                    self.lang_dic[each.language] += 1

        # Get Starred
        for each in self.user.get_starred():
            if each.language is not None:
                if each.language not in self.lang_dic:
                    self.lang_dic[each.language] = 1
                else:
                    self.lang_dic[each.language] += 1

    def main(self):
        self.analysis()
        languages = sorted(self.lang_dic, key=self.lang_dic.get, reverse=True)
        lang_str = ""
        for i in range(3):
            lang_str += languages[i]
            if i != 2:
                lang_str += ","
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'userid': self.username,
            'extract_language': lang_str,
            'keyword': ''
        }
        response = requests.post('http://angelbeats.tk:3000/api/v1/signup', headers=headers, data=data)
        # print(response.status_code, response.reason)
        self.user_text.write(lang_str)
        self.user_text.close()
        return languages


if __name__ == "__main__":
    start = time.time()
    name = input()
    s = Analysis(name)
    dic = s.main()
    # print(s.lang_dic)
    # print(dic)
    # print(time.time() - start)
