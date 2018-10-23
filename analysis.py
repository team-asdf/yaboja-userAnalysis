from github import Github


class Analysis:
    def __init__(self, username):
        f = open("/Users/ghyeon/Documents/token/token")
        token = f.readline().rstrip()
        github = Github(token)
        f.close()
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
        return self.lang_dic


if __name__ == "__main__":
    name = input("Username: ")
    s = Analysis(name)
    dic = s.main()
    print(dic)