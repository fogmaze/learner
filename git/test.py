from github import Github

if __name__ == '__main__':
    git = Github(login_or_token='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')
    repo = git.get_repo('fogmaze/learner')
    print(repo.get_topics())
    repo.create_file('yee.txt','hello',content="hi")
