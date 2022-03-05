import os
from github import Github
import base64


def getRepo()->Github:
    return Github(login_or_token='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').get_repo('fogmaze/learner')

def saveFile(file):
    if not os.path.isdir(os.path.dirname(file.path)) and os.path.dirname(file.path) != '':
        print(os.path.dirname(file.path))
        os.mkdir(os.path.dirname(file.path))
    with open(file.path,'w',encoding='utf-8') as f:
        f.write(base64.b64decode(contents.content).decode('utf8'))

def DownloadFolder(repo,path:str):
    repo.get_contents()

if __name__ == '__main__':
    repo = Github(login_or_token='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').get_repo('fogmaze/learner')
    contents = repo.get_contents(path='aaaa.txt')
    saveFile(contents)
    
